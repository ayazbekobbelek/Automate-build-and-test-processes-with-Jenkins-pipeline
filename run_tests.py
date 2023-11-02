import subprocess
import logging
import os
import sys

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


def build_tests(tests_dir, build_dir):
    # Create build directory if it does not exist
    os.makedirs(build_dir, exist_ok=True)

    # Run CMake to generate the build system in the build directory
    run_command(['cmake', tests_dir], build_dir)
    # Build the tests
    run_command(['cmake', '--build', '.'], build_dir)


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


if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: run_tests.py <tests_dir> <build_dir>")
        sys.exit(1)

    tests_dir = sys.argv[1]
    build_dir = sys.argv[2]
    main(tests_dir, build_dir)
