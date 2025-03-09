def list_tools():
    tools_available = """
-get_cwd: Get the current working directory
    Parameters: None. This tool does not need a parameter.
    Returns: String - information about the current working directory

-list_directory: List the contents of a directory in the filesystem
    Parameters:
    - path (optional, string): path of the directory to list. If not provided, lists the current working directory.
    Returns: String - a list of files and directories in the specified path
    
-read_file: Read a file in the filesystem
    Parameters:
    - path (required, string): path and filename of the file to read 
    Returns: String - the contents of the file specified in `path`

-write_file: Write content to a file in the filesystem
    Parameters:
    - path (required, string): path and filename of the file to write
    - content (required, string): the content to write to the file
    Returns: String - confirmation message indicating success or failure

-create_directory: Create a new directory in the filesystem
    Parameters:
    - path (required, string): path of the directory to create
    Returns: String - confirmation message indicating success or failure



"""
    return tools_available

def get_tools_format():
    
    tools_format = """

When you want to use a tool, make a tool call (no explanations) using this exact format:

[[qwen-tool-start]]
{
    "name": "tool_name",
    "input": {
        "param1": "value1",
        "param2": "value2"
    }
}
[[qwen-tool-end]]


Example 1:
************************
User: What is your current working directory?
Qwen-Max:
[[qwen-tool-start]]
{
    "name": "get_cwd",
    "input": ""
}
[[qwen-tool-end]]
**********************


Example 2:
************************
User: List the files in your current working directory.
Qwen-Max:
[[qwen-tool-start]]
{
    "name": "list_directory",
    "input": {
        "path": "."
    }
}
[[qwen-tool-end]]
**********************

Immediately end your response after calling a tool and the final triple backticks.

After receiving the results of a tool call, do not parrot everything back to the user.
Instead, just briefly summarize the results in 1-2 sentences.

"""
    return tools_format
