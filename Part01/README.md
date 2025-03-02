# Journey to Agentic AI, Starting From First Principles, Part 1: From Next-Token to Tool-Use: How to Give LLMs the Ability to Use Tools

## Original Blog Post
This repo is a companion to the [full article on Medium](https://medium.com/@jvroig/from-next-token-to-tool-use-how-to-give-llms-the-ability-to-use-tools-d26a2db2a9ae) that goes through the fundamentals of enabling LLMs to use tools.


## Overview

This repository provides a web-based chat interface and Python API backend that equips LLMs with tools. 

**Important Note**: This is an **educational implementation** designed to demonstrate how tool-calling works with Large Language Models (LLMs). It is **not intended for production use**. Please exercise caution when using this code, especially when interacting with sensitive filesystems. Always ensure proper security measures are in place if deploying similar solutions in real-world scenarios.

### Changing Endpoints and Models

Although the sample code defaults to hitting an Alibaba Cloud Model Studio endpoint in order to use a Qwen model (you’ll need an Alibaba Cloud account and valid Model Studio API Key), the code just uses standard OpenAI API-compatible calls, so you can swap it out for any other endpoint you want, including any vLLM, TGI, or llama.cpp server that you are running yourself, using any LLM you want.


### Features

- **Read Files**: Read the contents of files within the filesystem.

### Tools Description

1. **read-file**
    - **Description**: Read a file in the filesystem.
    - **Parameters**:
      - `path` (required, string): Path and filename of the file to read.
    - **Returns**: String - the contents of the file specified in `path`.

### Installation

To get started with this project, follow these steps:

1. **Clone this repository**
    
    Clone this repo, then go to the Part01 folder

    ```bash
    git clone https://github.com/jvroig/journey-to-agentic-ai-from-first-principles.git
    cd Part01
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

In your file browser, double-click the file index.html to load the chat interface in your default browser.

The web interface allows you to communicate with the LLM using natural language commands and tell it to use tools available.

As of Part 1, only 1 tool is available: read-file

"Read the file at path /example/path/to/file.txt."