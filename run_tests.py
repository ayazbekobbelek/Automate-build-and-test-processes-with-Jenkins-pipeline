import subprocess
import sys
import os
import logging

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_tests(test_executable):
    # Check if the test executable exists and is a file
    if not os.path.isfile(test_executable):
        logging.error(f"Test executable not found: {test_executable}")
        sys.exit(1)

    # Check if the test executable is runnable
    if not os.access(test_executable, os.X_OK):
        logging.error(f"Test executable is not runnable: {test_executable}")
        sys.exit(1)

    # Run the test executable
    result = subprocess.run(test_executable, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Log the output from the test
    logging.info(result.stdout.decode())

    # Check the exit code to determine if the tests passed
    if result.returncode == 0:
        logging.info("All tests passed.")
        return 0
    else:
        logging.error("Some tests failed.")
        return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python3 run_tests.py <path_to_test_executable>")
        sys.exit(1)

    # The first argument is the script name, the second argument is the test executable path
    test_executable = sys.argv[1]

    # Run the tests
    sys.exit(run_tests(test_executable))
