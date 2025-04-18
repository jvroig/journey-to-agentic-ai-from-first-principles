# Journey to Agentic AI, Starting From First Principles, Part 2: Giving Control of Our Computer to an LLM

## Original Blog Post
This repo is a companion to the original Medium article [Journey to Agentic AI, Starting From First Principles, Part 2: Giving Control of Our Computer to an LLM](https://medium.com/ai-advances/giving-control-of-our-computer-to-an-llm-48b93e8c6db1) by JV Roig, that goes through how to allow an LLM to take more actions in our computer. 


## Overview

This repository provides a web-based chat interface and Python API backend that equips LLMs with tools. 

**Important Note**: This is an **educational implementation** designed to demonstrate how tool-calling works with Large Language Models (LLMs). It is **not intended for production use**. Please exercise caution when using this code, especially when interacting with sensitive filesystems. Always ensure proper security measures are in place if deploying similar solutions in real-world scenarios.

### Changing Endpoints and Models

Although the sample code defaults to hitting an Alibaba Cloud Model Studio endpoint in order to use a Qwen model (you’ll need an Alibaba Cloud account and valid Model Studio API Key), the code just uses standard OpenAI API-compatible calls, so you can swap it out for any other endpoint you want, including any vLLM, TGI, or llama.cpp server that you are running yourself, using any LLM you want.

### Features

- **Get Current Working Directory**: Retrieve the current working directory.
- **Read Files**: Read the contents of files within the filesystem.
- **Write Files**: Write content to files in the filesystem.
- **Create Directories**: Create new directories in the filesystem.
- **List Directory Contents**: List all files and directories in a specified path (or the current working directory).

### Tool Descriptions

1. **get_cwd**
    - **Description**: Get the current working directory.
    - **Parameters**: None.
    - **Returns**: String - information about the current working directory.

2. **read_file**
    - **Description**: Read a file in the filesystem.
    - **Parameters**:
      - `path` (required, string): Path and filename of the file to read.
    - **Returns**: String - the contents of the file specified in `path`.

3. **write_file**
    - **Description**: Write content to a file in the filesystem.
    - **Parameters**:
      - `path` (required, string): Path and filename of the file to write.
      - `content` (required, string): The content to write to the file.
    - **Returns**: String - confirmation message indicating success or failure.

4. **create_directory**
    - **Description**: Create a new directory in the filesystem.
    - **Parameters**:
      - `path` (required, string): Path of the directory to create.
    - **Returns**: String - confirmation message indicating success or failure.

5. **list_directory**
    - **Description**: List the contents of a directory in the filesystem.
    - **Parameters**:
      - `path` (optional, string): Path of the directory to list. If not provided, lists the current working directory.
    - **Returns**: String - a list of files and directories in the specified path.


To get started with this project, follow these steps:

1. **Clone this repository**
    
    Clone this repo, then go to the Part02 folder

    ```bash
    git clone https://github.com/jvroig/journey-to-agentic-ai-from-first-principles.git
    cd Part02
    ```

1. **Set Up a Virtual Environment (Optional but Recommended)**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  
    # On Windows: venv\Scripts\activate
    ```

3. **Run the Backend API Server**

    ```bash
    python setup.py #this will install dependencies and create start.sh file
    bash start.sh #this will start the API server
    ```
    This will start the Python backend server on http://localhost:5001.

### Access the Web Interface

In your file browser, double-click the file Part02/index.html to load the chat interface in your default browser.

The web interface allows you to communicate with the LLM using natural language commands and tell it to use tools available.