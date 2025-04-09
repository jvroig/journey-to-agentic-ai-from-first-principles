def list_tools():
    tools_available = """
-get_cwd: Get the current working directory
    Parameters: None. This tool does not need a parameter.
    Returns: String - information about the current working directory

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

-list_directory: List the contents of a directory in the filesystem
    Parameters:
    - path (optional, string): path of the directory to list. If not provided, lists the current working directory.
    Returns: String - a list of files and directories in the specified path

-git_clone: Clone a git repository using HTTPS
    Parameters:
    - repo_url (required, string): The HTTPS URL of the repository to clone
    - target_path (optional, string): The path where to clone the repository
    Returns: String - confirmation message indicating success or failure

-git_commit: Stage all changes and create a commit
    Parameters:
    - message (required, string): The commit message
    - path (optional, string): The path to the git repository (defaults to current directory)
    Returns: String - confirmation message indicating success or failure

-git_restore: Restore the repository or specific files to a previous state
    Parameters:
    - commit_hash (optional, string): The commit hash to restore to. If not provided, unstages all changes
    - path (optional, string): The path to the git repository (defaults to current directory)
    - files (optional, list): List of specific files to restore. If not provided, restores everything
    Returns: String - confirmation message indicating success or failure

-git_push: Push commits to a remote repository
    Parameters:
    - remote (optional, string): The remote name (defaults to 'origin')
    - branch (optional, string): The branch name to push to (defaults to 'main')
    - path (optional, string): The path to the git repository (defaults to current directory)
    Returns: String - confirmation message indicating success or failure

-git_log: Get the commit history of the repository
    Parameters:
    - path (optional, string): The path to the git repository (defaults to current directory)
    - max_count (optional, integer): Maximum number of commits to return
    - since (optional, string): Get commits since this date (e.g., "2024-01-01" or "1 week ago")
    Returns: String - JSON formatted commit history with hash, author, date, and message for each commit

-git_show: Get detailed information about a specific commit
    Parameters:
    - commit_hash (required, string): The hash of the commit to inspect
    - path (optional, string): The path to the git repository (defaults to current directory)
    Returns: String - JSON formatted commit details including metadata and changed files

-git_status: Get the current status of the repository
    Parameters:
    - path (optional, string): The path to the git repository (defaults to current directory)
    Returns: String - JSON formatted repository status including staged, unstaged, and untracked changes

-git_diff: Get the differences between commits, staged changes, or working directory
    Parameters:
    - path (optional, string): The path to the git repository (defaults to current directory)
    - commit1 (optional, string): First commit hash for comparison
    - commit2 (optional, string): Second commit hash for comparison
    - staged (optional, boolean): If True, show staged changes (ignored if commits are specified)
    - file_path (optional, string): Path to specific file to diff
    Returns: String - JSON formatted diff information including:
        - Summary (files changed, total additions/deletions)
        - Detailed changes per file with hunks showing exact line modifications

-brave_web_search: Search the web using Brave Search API. The responses here only contain summaries. Use fetch_web_page to get the full contents of interesting search results.
    Parameters:
    - query (required, string): the search query to submit to Brave
    - count (optional, integer): the number of results to return, defaults to 10
    Returns: Object - a JSON object containing search results or error information from the Brave Search API

- fetch_web_page: Fetch content from a specified URL. This is a good tool to use after doing a brave_web_search, in order to get more details from interesting search results.
    Parameters:
    - url (required, string): the URL to fetch content from
    - headers (optional, dictionary): custom headers to include in the request, defaults to a standard User-Agent
    - timeout (optional, integer): request timeout in seconds, defaults to 30
    - clean (optional, boolean): whether to extract only the main content, defaults to True
    Returns: String - the cleaned web page content as text, or an error object if the request fails
"""
    return tools_available

def get_tools_format():
    
    tools_format = """

When you want to use a tool, make a tool call (no explanations) using this exact format:

```
[[qwen-tool-start]]
{
    "name": "tool_name",
    "input": {
        "param1": "value1",
        "param2": "value2"
    }
}
[[qwen-tool-end]]
```

Note that the triple backticks (```) are part of the format!

Example 1:
************************
User: What is your current working directory?
Qwen-Max:
```
[[qwen-tool-start]]
{
    "name": "get_cwd",
    "input": ""
}
[[qwen-tool-end]]
```
**********************


Example 2:
************************
User: List the files in your current working directory.
Qwen-Max:
```
[[qwen-tool-start]]
{
    "name": "list_directory",
    "input": {
        "path": "."
    }
}
[[qwen-tool-end]]
```
**********************

Immediately end your response after calling a tool and the final triple backticks.

After receiving the results of a tool call, do not parrot everything back to the user.
Instead, just briefly summarize the results in 1-2 sentences.

"""
    return tools_format
