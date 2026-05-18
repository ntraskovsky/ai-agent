import os


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_file_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        valid_file_path = not os.path.isdir(target_file)
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'
    

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content in a specified file at provided file path relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write content into, relative to the working directory. Cannot be an existing dir"
                },
                "content": {
                    "type": "string",
                    "description": "Data to write into the file"
                }
            },
            "required": []
        }
    }
}