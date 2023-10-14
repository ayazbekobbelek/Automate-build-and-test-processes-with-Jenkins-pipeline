# sync.py

import subprocess
import os


def run_git_command(command, repo_dir):
    """
    Run a Git command in the specified directory.
    """
    try:
        output = subprocess.check_output(['git'] + command, cwd=repo_dir)
        return output.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error while running git command: {e}")
        return None


def clone_repository(repo_url, destination_folder):
    """
    Clone the repository from repo_url to destination_folder.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    return run_git_command(['clone', repo_url, destination_folder], destination_folder)


def update_repository(repo_dir):
    """
    Pull the latest code in the specified repository directory.
    """
    # Fetch the latest changes
    fetch_result = run_git_command(['fetch'], repo_dir)
    if fetch_result is None:
        return None

    # Merge the latest changes
    merge_result = run_git_command(['merge'], repo_dir)
    return merge_result

# Example usage:
# clone_repository('https://github.com/your-repo.git', '/path/to/destination')
# update_repository('/path/to/repo_directory')
