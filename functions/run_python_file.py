import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        valid_file_path = os.path.isfile(target_file)
        if not valid_file_path:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        valid_file_path = target_file.endswith('.py')
        if not valid_file_path:
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)

        result = ""

        s_process = subprocess.run(
            args=command, 
            text=True, 
            timeout=30, 
            capture_output=True, 
            cwd=working_dir_abs
        )
        if s_process.returncode != 0:
            result += f"Process exited with code {s_process.returncode}"
        if not s_process.stdout and not s_process.stderr:
            result += "No output produced"
        elif s_process.stdout:
            result += f"STDOUT: {s_process.stdout}"
        elif s_process.stderr:
            result += f"STDERR: {s_process.stderr}"

        return result
    
    except Exception as e:
        return f"Error: executing Python file: {e}"

    
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs .py file at a specified file path relative to the working directory. Returns a result of execution",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to retrieve data from, relative to the working directory. Must point to a file, not a directory"
                },
                "args": {
                    "type": "array",
                    "description": "List of possible optional call arguments for a given .py file. Default is None"
                }
            },
            "required": []
        }
    }
}