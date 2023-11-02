import subprocess
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_command(command, working_dir):
    try:
        logging.info(f"Running command: {command} in directory {working_dir}")
        result = subprocess.run(command, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        logging.info(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{e.cmd}' failed with return code {e.returncode}")
        logging.error(e.output.decode())
        sys.exit(e.returncode)


def main(test_binary_dir, test_binary_name):
    test_binary_path = os.path.join(test_binary_dir, test_binary_name)
    if not os.path.exists(test_binary_path):
        logging.error(f"Test binary does not exist: {test_binary_path}")
        sys.exit(1)

    # Run the compiled test binary
    run_command([test_binary_path], test_binary_dir)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python3 run_tests.py <path_to_test_binary_dir> <test_binary_name>")
        sys.exit(1)

    test_binary_dir = sys.argv[1]
    test_binary_name = sys.argv[2]

    main(test_binary_dir, test_binary_name)
