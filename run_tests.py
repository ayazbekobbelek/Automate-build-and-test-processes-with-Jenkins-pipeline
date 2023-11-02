import subprocess
import logging
import os
import sys
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def run_command(command, working_dir):
    try:
        logging.info(f"Running command: {command}")
        result = subprocess.run(command, cwd=working_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True)
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{e.cmd}' failed with return code {e.returncode}")
        logging.error(e.output)
        sys.exit(e.returncode)


def build_tests(test_source_dir, test_build_dir, test_executable_dir):
    # Configure and build tests
    subprocess.run(['cmake', test_source_dir, '-B', test_build_dir])
    subprocess.run(['cmake', '--build', test_build_dir])

    # Find the test executable and move it to the desired directory
    test_executable = 'TEST'  # Replace with the actual executable name
    shutil.move(f'{test_build_dir}/{test_executable}', test_executable_dir)


def run_tests(build_dir):
    # Assuming the test executable is named 'test_executable'
    test_executable = os.path.join(build_dir, 'TEST')
    if not os.path.exists(test_executable):
        logging.error("Test executable not found.")
        sys.exit(1)

    # Run the tests
    run_command([test_executable], build_dir)


def main(tests_dir, build_dir):
    # Build the tests
    build_tests(tests_dir, build_dir)
    # Run the tests
    run_tests(build_dir)


if __name__ == '__main__':
    test_source_dir = sys.argv[1]
    test_build_dir = sys.argv[2]
    test_executable_dir = sys.argv[3]
    build_tests(test_source_dir, test_build_dir, test_executable_dir)
