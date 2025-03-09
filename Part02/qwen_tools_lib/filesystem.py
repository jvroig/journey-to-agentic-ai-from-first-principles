import os

def get_cwd():
    """
    Get the current working directory.
    
    Returns:
        str: The current working directory path.
    """
    try:
        return os.getcwd()
    except Exception as e:
        return f"Error getting current working directory: {e}"

def read_file(path):
    """
    Read the contents of a file.
    
    Args:
        path (str): The path to the file to read.
        
    Returns:
        str: The contents of the file, or an error message if reading fails.
    """
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {path}"
    except PermissionError:
        return f"Permission denied: {path}"
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(path, content):
    """
    Write content to a file.
    
    Args:
        path (str): The path to the file to write.
        content (str): The content to write to the file.
        
    Returns:
        str: A confirmation message, or an error message if writing fails.
    """
    try:
        with open(path, 'w') as file:
            file.write(content)
        return f"File written successfully: {path}"
    except PermissionError:
        return f"Permission denied: {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def create_directory(path):
    """
    Create a new directory.
    
    Args:
        path (str): The path of the directory to create.
        
    Returns:
        str: A confirmation message, or an error message if creation fails.
    """
    try:
        os.makedirs(path, exist_ok=True)  # `exist_ok=True` ensures no error if the directory already exists
        return f"Directory created successfully: {path}"
    except PermissionError:
        return f"Permission denied: {path}"
    except Exception as e:
        return f"Error creating directory: {e}"

def list_directory(path="."):
    """
    List the contents of a directory.
    
    Args:
        path (str): The path of the directory to list. Defaults to the current directory (".").
        
    Returns:
        str: A list of files and directories, or an error message if listing fails.
    """
    try:
        contents = os.listdir(path)
        return f"Contents of directory '{path}': {', '.join(contents)}"
    except FileNotFoundError:
        return f"Directory not found: {path}"
    except PermissionError:
        return f"Permission denied: {path}"
    except Exception as e:
        return f"Error listing directory: {e}"