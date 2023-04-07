import json
from langchain.agents import Tool
import os

def create_file_with_content(json_data: str) -> str:
    try:
        data = json.loads(json_data)
        path = data['path']
        content = data['content']
        with open(path, 'w') as file:
            file.write(content)
        return "Created file at " + path
    except Exception as e:
        return str(e)

def create_file_tool() -> Tool:
    return Tool(name="create_file", description="Create a file with the given content, requires a json string with 'path' and 'content' keys, path should be absolute", func=create_file_with_content)

def create_folder(path: str) -> str:
    try:
        os.mkdir(path)
        return "Created folder at " + path
    except Exception as e:
        return str(e)

def create_folder_tool() -> Tool:
    return Tool(name="create_folder", description="Create a folder, requires full path to the folder", func=create_folder)

def overwrite_file_with_content(json_data: str) -> str:
    try:
        data = json.loads(json_data)
        path = data['path']
        content = data['content']
        with open(path, 'w') as file:
            file.write(content)
        return "Overwrote file at " + path
    except Exception as e:
        return str(e)

def overwrite_file_tool() -> Tool:
    return Tool(name="overwrite_file", description="Overwrite a file with the given content, requires a json string with 'path' and 'content' keys, path should be absolute", func=overwrite_file_with_content)
