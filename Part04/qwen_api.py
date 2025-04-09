from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from openai import OpenAI
import os
import json
import qwen_tools_lib

from http import HTTPStatus
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# Load API Key
load_dotenv()
api_key = os.getenv('DASHSCOPE_API_KEY')
base_url = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'
#base_url = "http://127.0.0.1:8080"

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
            model="qwen-max-latest",
            messages=messages,
            stream=True
        )

        # # Extract the assistant's response
        # assistant_response = response.choices[0].message.content
        # print("Assistant Response:", assistant_response)
        # messages.append({"role": "assistant", "content": assistant_response})
        # yield json.dumps({'role': 'assistant', 'content': assistant_response}) + "\n"

        # FULL STREAMING CODE STUB
        assistant_response = ""

        # Iterate through the streaming response
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                # Get the text chunk
                content = chunk.choices[0].delta.content
                
                # Accumulate the full response
                assistant_response += content
                
                # Stream the chunk to the frontend
                yield json.dumps({'role': 'assistant', 'content': content, 'type': 'chunk'}) + "\n"

        # After streaming is complete, add the full response to messages
        messages.append({"role": "assistant", "content": assistant_response})

        # Send a completion signal
        yield json.dumps({'role': 'assistant', 'content': '', 'type': 'done'}) + "\n"


        occurrences = assistant_response.count("[[qwen-tool-start]]")
        if occurrences > 1:
            #Multiple tool calls are not allowed
            ToolErrorMsg="Tool Call Error: Multiple tool calls found. Please only use one tool at a time."
            yield json.dumps({'role': 'tool_call', 'content': ToolErrorMsg}) + "\n"

            messages.append({"role": "user", "content": ToolErrorMsg})
            print(ToolErrorMsg)
        elif occurrences == 1:
            tool_call_data = None
            try:
                tool_call_data = parse_tool_call(assistant_response)
            except:
                print(f"No valid tool call found")
                tool_message = f"Tool result: No valid tool call found. Please make sure tool request is valid JSON!"
                messages.append({"role": "user", "content": tool_message})
                yield json.dumps({'role': 'tool_call', 'content': tool_message}) + "\n"

            if tool_call_data:
                # Stream the tool call message back to the frontend
                # yield json.dumps({'role': 'tool_call', 'content': f"Tool call: {tool_call_data}"}) + "\n"

                # Execute the tool with the provided parameters
                tool_name = tool_call_data["name"]
                tool_input = tool_call_data.get("input", {})
                print(f"Executing tool: {tool_name} with input: {tool_input}")
                
                # Assume `execute_tool` is a predefined function
                tool_result = execute_tool(tool_name, tool_input)

                # Add the tool result as a "user" message in the conversation
                tool_message = f"Tool result: ```{tool_result}```"
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

    tools_available = qwen_tools_lib.list_tools()
    tools_format = qwen_tools_lib.get_tools_format()
    print(tools_available)
    print(tools_format)
    system_prompt = f"""You are Qwen-Max, an advanced AI model. You will assist the user with tasks, using tools available to you.

You have the following tools available:
{tools_available}

{tools_format}

"""
    system_message = {"role": "system", "content": system_prompt}
    messages.insert(0, system_message)

    return {'messages': messages, 'model': model, 'endpoint': endpoint } 

def parse_tool_call(response):
    """
    Parses the tool call information from an LLM response.
    
    Args:
        response (str): The LLM's response containing the tool call.
        
    Returns:
        dict: A dictionary containing the tool name and input parameters.
              Example: {"name": "tool_name", "input": {"param1": "value1", "param2": "value2"}}
              
    Raises:
        ValueError: If the tool call format is invalid or cannot be parsed.
    """
    # Define markers for the tool call block
    start_marker = "[[qwen-tool-start]]"
    end_marker = "[[qwen-tool-end]]"
    
    try:
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

    except json.JSONDecodeError as e:
        print(f"Failed to parse tool call JSON: {e}. Please make sure the tool call is valid JSON")
        raise
    
    except ValueError as e:
        print(f"Value Error: {e}.")
        raise

def execute_tool(tool_name, tool_input):
    """
    Executes the specified tool with the given input parameters.

    Args:
        tool_name (str): The name of the tool to execute.
        tool_input (dict): A dictionary containing the input parameters for the tool.

    Returns:
        str: The result of the tool execution.

    Raises:
        ValueError: If the tool_name is invalid or the tool function raises an error.
    """

    # Check if the tool exists
    if hasattr(qwen_tools_lib, tool_name):
        tool = getattr(qwen_tools_lib, tool_name)
        if callable(tool):
            pass
        else:
            raise ValueError(f"Unknown tool or uncallable tool: {tool_name}")
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

    try:
        # Execute the tool function with the provided input
        if tool_input == "":
            result = tool()
        else:
            result = tool(**tool_input)
        return result
    except Exception as e:
        raise ValueError(f"Error executing tool '{tool_name}': {e}")

if __name__ == '__main__':
    app.run(debug=True, port="5001")
