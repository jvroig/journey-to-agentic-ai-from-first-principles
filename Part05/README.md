# The Power of Tool Descriptions: Making Better LLM Tools + Research Power 

## Original Blog Post
This repo is a companion to the original Medium article [Journey to Agentic AI, Starting From First Principles, Part 5: Making Better LLM Tools + Research Power ]() by JV Roig, that goes through how to allow an LLM to take more actions in our computer. 


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
- **Git Operations**: Perform various Git operations such as cloning repositories, committing changes, and viewing commit history.

### Tools Description

1. **get-cwd**
    - **Description**: Get the current working directory.
    - **Parameters**: None.
    - **Returns**: String - information about the current working directory.

2. **read-file**
    - **Description**: Read a file in the filesystem.
    - **Parameters**:
      - `path` (required, string): Path and filename of the file to read.
    - **Returns**: String - the contents of the file specified in `path`.

3. **write-file**
    - **Description**: Write content to a file in the filesystem.
    - **Parameters**:
      - `path` (required, string): Path and filename of the file to write.
      - `content` (required, string): The content to write to the file.
    - **Returns**: String - confirmation message indicating success or failure.

4. **create-directory**
    - **Description**: Create a new directory in the filesystem.
    - **Parameters**:
      - `path` (required, string): Path of the directory to create.
    - **Returns**: String - confirmation message indicating success or failure.

5. **list-directory**
    - **Description**: List the contents of a directory in the filesystem.
    - **Parameters**:
      - `path` (optional, string): Path of the directory to list. If not provided, lists the current working directory.
    - **Returns**: String - a list of files and directories in the specified path.

6. **git-clone**
    - **Description**: Clone a git repository using HTTPS.
    - **Parameters**:
      - `repo_url` (required, string): The HTTPS URL of the repository to clone.
      - `target_path` (optional, string): The path where to clone the repository.
    - **Returns**: String - confirmation message indicating success or failure.

7. **git-commit**
    - **Description**: Stage all changes and create a commit.
    - **Parameters**:
      - `message` (required, string): The commit message.
      - `path` (optional, string): The path to the git repository (defaults to current directory).
    - **Returns**: String - confirmation message indicating success or failure.

8. **git-restore**
    - **Description**: Restore the repository or specific files to a previous state.
    - **Parameters**:
      - `commit_hash` (optional, string): The commit hash to restore to. If not provided, unstages all changes.
      - `path` (optional, string): The path to the git repository (defaults to current directory).
      - `files` (optional, list): List of specific files to restore. If not provided, restores everything.
    - **Returns**: String - confirmation message indicating success or failure.

9. **git-push**
    - **Description**: Push commits to a remote repository.
    - **Parameters**:
      - `remote` (optional, string): The remote name (defaults to 'origin').
      - `branch` (optional, string): The branch name to push to (defaults to 'main').
      - `path` (optional, string): The path to the git repository (defaults to current directory).
    - **Returns**: String - confirmation message indicating success or failure.

10. **git-log**
    - **Description**: Get the commit history of the repository.
    - **Parameters**:
      - `path` (optional, string): The path to the git repository (defaults to current directory).
      - `max_count` (optional, integer): Maximum number of commits to return.
      - `since` (optional, string): Get commits since this date (e.g., "2024-01-01" or "1 week ago").
    - **Returns**: String - JSON formatted commit history with hash, author, date, and message for each commit.

11. **git-show**
    - **Description**: Get detailed information about a specific commit.
    - **Parameters**:
      - `commit_hash` (required, string): The hash of the commit to inspect.
      - `path` (optional, string): The path to the git repository (defaults to current directory).
    - **Returns**: String - JSON formatted commit details including metadata and changed files.

12. **git-status**
    - **Description**: Get the current status of the repository.
    - **Parameters**:
      - `path` (optional, string): The path to the git repository (defaults to current directory).
    - **Returns**: String - JSON formatted repository status including staged, unstaged, and untracked changes.

13. **git-diff**
    - **Description**: Get the differences between commits, staged changes, or working directory.
    - **Parameters**:
      - `path` (optional, string): The path to the git repository (defaults to current directory).
      - `commit1` (optional, string): First commit hash for comparison.
      - `commit2` (optional, string): Second commit hash for comparison.
      - `staged` (optional, boolean): If True, show staged changes (ignored if commits are specified).
      - `file_path` (optional, string): Path to specific file to diff.
    - **Returns**: String - JSON formatted diff information including:
        - Summary (files changed, total additions/deletions)
        - Detailed changes per file with hunks showing exact line modifications.


To get started with this project, follow these steps:

1. **Clone this repository**
    
    Clone this repo, then go to the Part03 folder

    ```bash
    git clone https://github.com/jvroig/journey-to-agentic-ai-from-first-principles.git
    cd Part03
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

In your file browser, double-click the file Part03/index.html to load the chat interface in your default browser.

The web interface allows you to communicate with the LLM using natural language commands and tell it to use tools available.