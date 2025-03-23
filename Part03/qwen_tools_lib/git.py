import subprocess
from typing import Optional, Dict, List
import json
from datetime import datetime

def git_clone(repo_url: str, target_path: Optional[str] = None) -> str:
    """
    Clone a git repository using HTTPS.
    
    Args:
        repo_url (str): The HTTPS URL of the repository to clone
        target_path (str, optional): The path where to clone the repository
        
    Returns:
        str: A confirmation message, or an error message if cloning fails
    """
    try:
        cmd = ["git", "clone", repo_url]
        if target_path:
            cmd.append(target_path)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"Repository cloned successfully from {repo_url}"
        else:
            return f"Error cloning repository: {result.stderr}"
    except Exception as e:
        return f"Error during git clone: {str(e)}"

def git_commit(message: str, path: str = ".") -> str:
    """
    Stage all changes and create a commit.
    
    Args:
        message (str): The commit message
        path (str): The path to the git repository
        
    Returns:
        str: A confirmation message, or an error message if commit fails
    """
    try:
        # First stage all changes
        stage_cmd = ["git", "-C", path, "add", "."]
        stage_result = subprocess.run(stage_cmd, capture_output=True, text=True)
        
        if stage_result.returncode != 0:
            return f"Error staging changes: {stage_result.stderr}"
        
        # Then commit
        commit_cmd = ["git", "-C", path, "commit", "-m", message]
        commit_result = subprocess.run(commit_cmd, capture_output=True, text=True)
        
        if commit_result.returncode == 0:
            return "Changes committed successfully"
        else:
            return f"Error committing changes: {commit_result.stderr}"
    except Exception as e:
        return f"Error during git commit: {str(e)}"

def git_restore(commit_hash: Optional[str] = None, path: str = ".", files: Optional[list] = None) -> str:
    """
    Restore the repository or specific files to a previous state.
    
    Args:
        commit_hash (str, optional): The commit hash to restore to. If None, unstages all changes
        path (str): The path to the git repository
        files (list, optional): List of specific files to restore. If None, restores everything
        
    Returns:
        str: A confirmation message, or an error message if restore fails
    """
    try:
        cmd = ["git", "-C", path]
        
        if commit_hash:
            cmd.extend(["reset", "--hard", commit_hash])
        else:
            cmd.extend(["restore", "--staged", "."])
            if files:
                cmd.extend(files)
            else:
                cmd.append(".")
                
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if commit_hash:
                return f"Repository restored to commit {commit_hash}"
            else:
                return "Changes restored successfully"
        else:
            return f"Error restoring changes: {result.stderr}"
    except Exception as e:
        return f"Error during git restore: {str(e)}"

def git_push(remote: str = "origin", branch: str = "main", path: str = ".") -> str:
    """
    Push commits to a remote repository.
    
    Args:
        remote (str): The remote name (default: 'origin')
        branch (str): The branch name to push to (default: 'main')
        path (str): The path to the git repository
        
    Returns:
        str: A confirmation message, or an error message if push fails
    """
    try:
        cmd = ["git", "-C", path, "push", remote, branch]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"Successfully pushed to {remote}/{branch}"
        else:
            return f"Error pushing changes: {result.stderr}"
    except Exception as e:
        return f"Error during git push: {str(e)}"

def git_log(path: str = ".", max_count: Optional[int] = None, since: Optional[str] = None) -> str:
    """
    Get the commit history of the repository.
    
    Args:
        path (str): The path to the git repository
        max_count (int, optional): Maximum number of commits to return
        since (str, optional): Get commits since this date (e.g., "2024-01-01" or "1 week ago")
        
    Returns:
        str: JSON string containing commit history, or an error message if the operation fails
    """
    try:
        # Format each commit as a complete JSON object
        cmd = ["git", "-C", path, "log", "--pretty=format:%H%n%h%n%an%n%ai%n%s%n===="]
        
        if max_count:
            cmd.extend(["-n", str(max_count)])
        if since:
            cmd.extend(["--since", since])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Split the output into individual commits
            commits_raw = result.stdout.split("\n====\n")
            commits = []
            
            for commit_raw in commits_raw:
                if not commit_raw.strip():
                    continue
                
                # Split the commit data into its components
                parts = commit_raw.strip().split("\n")
                if len(parts) >= 5:
                    commit = {
                        "hash": parts[0],
                        "short_hash": parts[1],
                        "author": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    }
                    commits.append(commit)
            
            return json.dumps(commits, indent=2)
        else:
            return f"Error getting commit history: {result.stderr}"
    except Exception as e:
        return f"Error during git log: {str(e)}"

def git_show(commit_hash: str, path: str = ".") -> str:
    """
    Get detailed information about a specific commit.
    
    Args:
        commit_hash (str): The hash of the commit to inspect
        path (str): The path to the git repository
        
    Returns:
        str: JSON string containing detailed commit information, or an error message if the operation fails
    """
    try:
        # Get commit metadata as separate fields
        meta_cmd = ["git", "-C", path, "show", "-s", 
                   "--format=%H%n%an%n%ai%n%B", commit_hash]
        
        meta_result = subprocess.run(meta_cmd, capture_output=True, text=True)
        
        # Get changed files
        files_cmd = ["git", "-C", path, "show", "--name-status", "--format=", commit_hash]
        files_result = subprocess.run(files_cmd, capture_output=True, text=True)
        
        if meta_result.returncode == 0 and files_result.returncode == 0:
            # Parse the metadata
            meta_parts = meta_result.stdout.split('\n', 3)
            
            # Create commit info dict manually to avoid JSON parsing issues
            commit_info = {
                "hash": meta_parts[0],
                "author": meta_parts[1],
                "date": meta_parts[2],
                "message": meta_parts[3].strip() if len(meta_parts) > 3 else ""
            }
            
            # Parse the changed files
            changed_files = []
            for line in files_result.stdout.strip().split('\n'):
                if line:
                    status, *filepath = line.split('\t')
                    changed_files.append({
                        "status": status,
                        "path": filepath[0]
                    })
            
            # Combine the information
            commit_info["changed_files"] = changed_files
            return json.dumps(commit_info, indent=2)
        else:
            return f"Error getting commit details: {meta_result.stderr or files_result.stderr}"
    except Exception as e:
        return f"Error during git show: {str(e)}"

def git_status(path: str = ".") -> str:
    """
    Get the current status of the repository.
    
    Args:
        path (str): The path to the git repository
        
    Returns:
        str: JSON string containing repository status, or an error message if the operation fails
    """
    try:
        # Get status in porcelain format for easier parsing
        cmd = ["git", "-C", path, "status", "--porcelain", "-b"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            branch_info = lines[0].replace("## ", "")
            
            status_info = {
                "branch": branch_info,
                "staged": [],
                "unstaged": [],
                "untracked": []
            }
            
            for line in lines[1:]:
                if not line:
                    continue
                    
                status = line[:2]
                file_path = line[3:]
                
                if status[0] != ' ' and status[0] != '?':
                    status_info["staged"].append({
                        "status": status[0],
                        "path": file_path
                    })
                if status[1] != ' ':
                    status_info["unstaged"].append({
                        "status": status[1],
                        "path": file_path
                    })
                if status == "??":
                    status_info["untracked"].append(file_path)
            
            return json.dumps(status_info, indent=2)
        else:
            return f"Error getting repository status: {result.stderr}"
    except Exception as e:
        return f"Error during git status: {str(e)}"
    

def git_diff(path: str = ".", commit1: Optional[str] = None, commit2: Optional[str] = None, 
            staged: bool = False, file_path: Optional[str] = None) -> str:
    """
    Get the differences between commits, staged changes, or working directory.
    
    Args:
        path (str): The path to the git repository
        commit1 (str, optional): First commit hash for comparison
        commit2 (str, optional): Second commit hash for comparison
        staged (bool): If True, show staged changes (ignored if commits are specified)
        file_path (str, optional): Path to specific file to diff
        
    Returns:
        str: JSON string containing structured diff information, or an error message if diff fails
    """
    try:
        cmd = ["git", "-C", path, "diff", "--unified=3"]
        
        # Configure the diff command based on parameters
        if commit1 and commit2:
            cmd.extend([commit1, commit2])
        elif commit1:
            cmd.append(commit1)
        elif staged:
            cmd.append("--staged")
            
        if file_path:
            cmd.append("--")
            cmd.append(file_path)
            
        # Get the raw diff
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Parse the diff output into a structured format
            diff_lines = result.stdout.split('\n')
            current_file = None
            diffs = []
            current_diff = None
            current_hunk = None
            
            for line in diff_lines:
                if line.startswith('diff --git'):
                    if current_diff:
                        if current_hunk:
                            current_diff['hunks'].append(current_hunk)
                        diffs.append(current_diff)
                    current_diff = {'file': line.split(' b/')[-1], 'hunks': []}
                    current_hunk = None
                elif line.startswith('@@'):
                    if current_hunk:
                        current_diff['hunks'].append(current_hunk)
                    # Parse the hunk header (e.g., @@ -1,7 +1,6 @@)
                    parts = line.split('@@')[1].strip().split(' ')
                    current_hunk = {
                        'header': line,
                        'old_start': int(parts[0].split(',')[0].strip('-')),
                        'new_start': int(parts[1].split(',')[0].strip('+')),
                        'changes': []
                    }
                elif current_hunk is not None:
                    if line:
                        change_type = line[0]
                        if change_type in ['+', '-', ' ']:
                            current_hunk['changes'].append({
                                'type': change_type,
                                'content': line[1:]
                            })
            
            # Add the last hunk and diff
            if current_diff and current_hunk:
                current_diff['hunks'].append(current_hunk)
                diffs.append(current_diff)
            
            # Create a summary
            summary = {
                'files_changed': len(diffs),
                'total_additions': sum(
                    sum(1 for change in hunk['changes'] if change['type'] == '+')
                    for diff in diffs
                    for hunk in diff['hunks']
                ),
                'total_deletions': sum(
                    sum(1 for change in hunk['changes'] if change['type'] == '-')
                    for diff in diffs
                    for hunk in diff['hunks']
                )
            }
            
            return json.dumps({
                'summary': summary,
                'diffs': diffs
            }, indent=2)
        else:
            return f"Error getting diff: {result.stderr}"
    except Exception as e:
        return f"Error during git diff: {str(e)}"