# sync.py

import subprocess
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_git_command(command, repo_dir):
    """
    Run a Git command in the specified directory.
    """
    try:
        logging.info(f"Running git command: {' '.join(command)} in {repo_dir}")
        output = subprocess.check_output(['git'] + command, cwd=repo_dir)
        return output.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while running git command: {e}")
        return None


def clone_repository(repo_url, destination_folder):
    """
    Clone the repository from repo_url to destination_folder.
    """
    logging.info(f"Cloning repository from {repo_url} to {destination_folder}")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    return run_git_command(['clone', repo_url, destination_folder], destination_folder)


def update_repository(repo_dir):
    """
    Pull the latest code in the specified repository directory.
    """
    logging.info(f"Updating repository at {repo_dir}")

    # Fetch the latest changes
    fetch_result = run_git_command(['fetch'], repo_dir)
    if fetch_result is None:
        logging.error("Fetching latest changes failed")
        return None

    # Merge the latest changes
    merge_result = run_git_command(['merge'], repo_dir)
    if merge_result is None:
        logging.error("Merging latest changes failed")
    return merge_result


def main():
    if len(sys.argv) < 2:
        logging.error("Usage: sync.py [clone|update] [repository_url] [destination_folder]")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == 'clone':
        if len(sys.argv) != 4:
            logging.error("Usage: sync.py clone [repository_url] [destination_folder]")
            sys.exit(1)
        repo_url = sys.argv[2]
        destination_folder = sys.argv[3]
        clone_repository(repo_url, destination_folder)

    elif action == 'update':
        if len(sys.argv) != 3:
            logging.error("Usage: sync.py update [repository_folder]")
            sys.exit(1)
        repo_folder = sys.argv[2]
        update_repository(repo_folder)

    else:
        logging.error("Invalid action. Use 'clone' or 'update'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
