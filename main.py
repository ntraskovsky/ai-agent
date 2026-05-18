from openai import OpenAI
import os, sys
from dotenv import load_dotenv
import argparse
from rich import print
import json

from prompts import system_prompt
from functions.call_function import available_functions, call_function
from config import AGENT_LOOP_LIMIT

load_dotenv()
API_KEY = os.environ.get('GEMINI_API_KEY')


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    include_verbose = args.verbose

    client = OpenAI(
    base_url="https://routellm.abacus.ai/v1",
    api_key=API_KEY,
    )
    
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    print(f"[bold]User prompt:[/bold] {user_prompt}")

    for _ in range(AGENT_LOOP_LIMIT):
        chat_completion = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages,
        tools=available_functions,
        stream_options={"include_usage": True}
        )

        if include_verbose and chat_completion.usage:
            print(f"[bold]Prompt tokens:[/bold] {chat_completion.usage.input_tokens}")
            print(f"[bold]Response tokens:[/bold] {chat_completion.usage.output_tokens}")

        choice = chat_completion.choices[0]

        # appending model answer in history
        messages.append(choice.message)

        # if no tool_calls its a final answer
        if not choice.message.tool_calls:
            print(f"\n[bold green]Final response:[/bold green]\n{choice.message.content}")
            return

        # processing tool_calls
        function_results = []

        for tc in choice.message.tool_calls:
            tool = {
                "id": tc.id,
                "name": tc.function.name,
                "arguments": json.loads(tc.function.arguments or "{}"),
            }

            result = call_function(tool, verbose=include_verbose)

            content = result.get("content")
            if not content:
                raise Exception(f"Function {tool['name']} returned empty content")

            parsed = json.loads(content)
            if parsed is None:
                raise Exception(f"Function {tool['name']} returned None response")

            if include_verbose:
                print(f"-> {parsed}")

            function_results.append(result)

        # adding tool calls to history
        messages.extend(function_results)

    # AGENT_LOOP_LIMIT is reached
    print("[bold red]Error:[/bold red] Max iterations reached without a final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()
