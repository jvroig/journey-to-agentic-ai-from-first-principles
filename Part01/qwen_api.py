from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from openai import OpenAI
import os
import json
# import yaml

import random
from http import HTTPStatus
from dashscope import Generation
import dashscope
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

# Load API Key
load_dotenv()
api_key = os.getenv('DASHSCOPE_API_KEY')
base_url = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'

@app.route('/api/chat', methods=['POST'])
def query_endpoint():
    try:
        # Parse JSON payload from the request
        payload = request.get_json()
        messages = payload.get('messages', [])
        temperature = payload.get('temperature', 0.4)
        max_output_tokens = payload.get('max_output_tokens', 1000)

        # Format messages (you can replace this with your actual logic)
        data = format_messages(messages)
        messages = data['messages']

        print("Received messages:", messages)

        # Use a generator to stream responses back to the frontend
        def generate_responses():
            yield from inference_loop(messages)

        # Return a streaming response with the correct content type
        return Response(generate_responses(), content_type='text/event-stream')

    except Exception as e:
        # Handle errors gracefully
        return {"error": str(e)}, 400


def inference_loop(messages):
    while True:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        response = client.chat.completions.create(
            model="qwen2.5-72b-instruct",
            messages=messages,
        )

        # Extract the assistant's response
        assistant_response = response.choices[0].message.content
        print("Assistant Response:", assistant_response)

        # Add the assistant's response to the messages list
        messages.append({"role": "assistant", "content": assistant_response})

        # Stream the assistant's response back to the frontend
        yield json.dumps({'role': 'assistant', 'content': assistant_response}) + "\n"

        # Check if the response contains a tool call
        tool_call_data = None
        try:
            tool_call_data = parse_tool_call(assistant_response)
        except ValueError as e:
            print(f"No valid tool call found: {e}")

        if tool_call_data:
            # Stream the tool call message back to the frontend
            yield json.dumps({'role': 'tool_call', 'content': f"Tool call: {tool_call_data}"}) + "\n"

            # Execute the tool with the provided parameters
            tool_name = tool_call_data["name"]
            tool_input = tool_call_data.get("input", {})
            print(f"Executing tool: {tool_name} with input: {tool_input}")
            
            # Assume `execute_tool` is a predefined function
            tool_result = execute_tool(tool_name, tool_input)

            # Add the tool result as a "user" message in the conversation
            tool_message = f"Tool result: {tool_result}"
            messages.append({"role": "user", "content": tool_message})
            print(f"Tool executed. Result: {tool_result}")

            # Stream the tool result back to the frontend
            yield json.dumps({'role': 'tool_call', 'content': tool_message}) + "\n"
        else:
            # If no tool call, terminate the loop
            break

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

    system_message = {"role": "system", "content": system_prompt}
    messages.insert(0, system_message)

    return {'messages': messages, 'model': model, 'endpoint': endpoint } 


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
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {path}"
    except PermissionError:
        return f"Permission denied: {path}"
    except Exception as e:
        return f"Error reading file: {e}"

if __name__ == '__main__':
    app.run(debug=True, port="5001")
