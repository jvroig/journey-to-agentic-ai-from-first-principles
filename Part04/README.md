# Journey to Agentic AI, Starting From First Principles, Part 4: MCP in Action, Some Mythbusting and Security Nightmares

## Original Blog Post
This repo is a companion to the original Medium article [Journey to Agentic AI, Starting From First Principles, Part 4: MCP in Action, Some Mythbusting and Security Nightmares](https://medium.com/ai-advances/journey-to-agentic-ai-part-4-mcp-in-action-some-mythbusting-and-security-nightmares-7d990f8db3ef) by JV Roig, that goes through how to connect to external services like GitHub, and be able to execute local git operations.


## Overview

There isn't specific code for this part, but this is a good opportunity to review fundamental principles about tool-calling to understand how and why MCP can be a security nightmare.

Here's a quick recap of how tools information (*how to invoke tools, specific tool descriptions and syntax and parameters...*) are purposely sent to the LLM's system prompt in order for tool-calling to work.

In our usual code (available in Parts 1 - 3 of this monorepo), we have this in our `qwen_api.py` file:
```python
def format_messages(messages):
    model = ''
    endpoint = ''

    system_prompt = """You are Qwen-Max, an advanced AI model. 
You will assist the user with tasks, using tools available to you.

You have the following tools available:
-read-file: Read a file in the filesystem
    Parameters:
    - path (required, string): path and filename of the file to read 
    Returns: String - the contents of the file specified in `path`

When you want to use a tool, make a tool call (no explanations) 
using this exact format:

[[qwen-tool-start]]
{
    "name": "tool_name",
    "input": {
        "param1": "value1",
        "param2": "value2"
    }
}
[[qwen-tool-end]]

Example:
************************
User: Can you tell me what's inside /home/user/readme.txt?
Qwen-Max:
[[qwen-tool-start]]
{
    "name": "read-file",
    "input": "/home/user/readme.txt"
}
[[qwen-tool-end]]
**********************
"""
...
```
This code is responsible for teaching our LLM how to properly ask for tools, the list of tools it has, and the syntax and argument information for the tool. 

This snippet was taken from Part 1, where we started with a single tool (`read-file`).

Parts 2 and 3 expand on this by adding more tools, and making the prompt a bit more dynamically created instead of fully static, but the spirit is the same: **Giving an LLM some tools means adding a bunch of text into its system prompt!**

And this is the first reason why MCP can be security nightmare - connecting to third-party MCP servers you haven't vetted will mean you are allowing these MCP servers to inject arbitrary instructions to your LLM, which, if they were malicious, could be poisoning your LLMs context and turning it into a malicious actor.

That's not all. Let's review how the `read-file` tool is implemented:
```python
def parse_tool_call(response):
    # Define markers for the tool call block
    start_marker = "[[qwen-tool-start]]"
    end_marker = "[[qwen-tool-end]]"
    
    # Extract the JSON block between the markers
    start_index = response.find(start_marker) + len(start_marker)
    end_index = response.find(end_marker)
    
    if start_index == -1 or end_index == -1:
        raise ValueError("Tool call markers not found in the response.")
    
    tool_call_block = response[start_index:end_index].strip()
    
    # Parse the JSON content
    tool_call_data = json.loads(tool_call_block)
    
    # Validate the structure of the tool call
    if "name" not in tool_call_data:
        raise ValueError("Tool call must include a 'name' field.")

    return tool_call_data


def execute_tool(tool_name, tool_input):
    # Map tool names to their respective functions
    tool_functions = {
        "read-file": read_file,
    }

    # Retrieve the tool function
    tool_function = tool_functions[tool_name]

    try:
        # Execute the tool function with the provided input
        result = tool_function(**tool_input)
        return result
    except Exception as e:
        raise ValueError(f"Error executing tool '{tool_name}': {e}")

def read_file(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {path}"
    except PermissionError:
        return f"Permission denied: {path}"
    except Exception as e:
        return f"Error reading file: {e}"
```
In the snippets above, you can see most of the typical flow for handling a tool call.

- `parse_tool_call` finds out if an LLM response includes a tool request.
- `execute_tool` will be sent the tool request, and will find the correct tool implementation to execute based on the request
- `read_file` is the tool in our example, and is called by `execute_tool`.

As you can see, the ultimate tool itself - `read_file` - is nothing more than just another function or program we are executing on behalf of an LLM's request.

This means, when you run MCP servers from third-parties on your local machine (which is how most of the first MCP servers are implemented), you are essentially allowing **arbitrary code execution** - you are trusting that this MCP server isn't also doing malicious things like running malware or siphoning off secrets and creds from your machine.

These two very real dangers make MCP a security nightmare for the unprepared.