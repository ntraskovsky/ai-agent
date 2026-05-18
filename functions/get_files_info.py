import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        search_dir_name = "current" if target_dir == working_dir_abs else f"'{directory}'"
        print(f"Result for {search_dir_name} directory:")

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        valid_target_dir = os.path.isdir(target_dir)
        if not valid_target_dir:
            return f'Error: "{directory}" is not a directory'
        
        # return f'Success: "{directory}" is within the working directory'

        result = ""
        
        target_dir_content = os.listdir(target_dir)
        for item in target_dir_content:
            item_path = os.path.join(target_dir, item)
            item_info = f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            print(item_info)
            result += item_info + "\n"

        return result
    
    except Exception as e:
        return f'Error: {e}'


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)"
                }
            },
            "required": []
        }
    }
}