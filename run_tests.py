import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def run_command(command, working_dir):
    """Run a shell command in a specific directory and log the output."""
    try:
        logging.info(f"Running command: {' '.join(command)} in directory {working_dir}")
        result = subprocess.run(command, cwd=working_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with return code {e.returncode}")
        logging.error(e.output.decode())
        sys.exit(e.returncode)

def run_tests(build_dir):
    """Run all Google Test unit tests."""
    test_executable = os.path.join(build_dir, 'your_test_executable')  # Replace with your actual test executable name
    if not os.path.isfile(test_executable):
        logging.error(f"Test executable not found: {test_executable}")
        sys.exit(1)

    run_command([test_executable], build_dir)

def main():
    if len(sys.argv) != 2:
        logging.error("Usage: python3 run_tests.py <build_dir>")
        sys.exit(1)

    build_dir = sys.argv[1]
    if not os.path.isdir(build_dir):
        logging.error(f"Build directory does not exist: {build_dir}")
        sys.exit(1)

    run_tests(build_dir)

if __name__ == "__main__":
    main()
