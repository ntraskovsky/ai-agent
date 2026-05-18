import os
from config import FILE_READ_BYTES_LIMIT


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        valid_file_path = os.path.isfile(target_file)
        if not valid_file_path:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # max amount of chars to read from file
        with open(target_file, 'r') as file:
            content = file.read(FILE_READ_BYTES_LIMIT)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {FILE_READ_BYTES_LIMIT} characters]'
        
        return content
    
    except Exception as e:
        return f'Error: {e}'
    

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns content of a file at a specified file path relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to retrieve data from, relative to the working directory. Must point to a file, not a directory"
                }
            },
            "required": []
        }
    }
}