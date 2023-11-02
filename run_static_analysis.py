import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.FileHandler("static_analysis.log"),
                        logging.StreamHandler(sys.stdout)
                    ])

def run_command(command, working_dir='.'):
    """Run a shell command and log the output."""
    try:
        logging.info(f"Running command: {' '.join(command)} in {working_dir}")
        result = subprocess.run(command, cwd=working_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with return code {e.returncode}")
        logging.error(e.output.decode())
        sys.exit(e.returncode)

def run_cppcheck(source_dir):
    """Run cppcheck static code analysis."""
    command = ['cppcheck', '--enable=all', '--suppress=missingInclude', source_dir]
    run_command(command)

def main():
    if len(sys.argv) != 2:
        logging.error("Usage: python3 run_static_analysis.py <source_dir>")
        sys.exit(1)

    source_dir = sys.argv[1]
    if not os.path.isdir(source_dir):
        logging.error(f"Source directory does not exist: {source_dir}")
        sys.exit(1)

    run_cppcheck(source_dir)

if __name__ == "__main__":
    main()
