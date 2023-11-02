import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def run_command(command, working_dir):
    """Run a shell command in a specific directory and log the output."""
    try:
        logging.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, cwd=working_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with return code {e.returncode}")
        logging.error(e.output.decode())
        sys.exit(e.returncode)


def compile_tests(tests_dir, build_dir):
    """Compile the tests using CMake."""
    test_build_dir = os.path.join(build_dir, "test", "build")
    if not os.path.exists(test_build_dir):
        os.makedirs(test_build_dir)

    # Run CMake to configure the project for tests
    run_command(['cmake', tests_dir], test_build_dir)

    # Build the tests
    run_command(['cmake', '--build', '.'], test_build_dir)

    # The name of your test executable (replace 'your_test_executable_name' with the actual name)
    test_executable_name = 'TEST'
    test_executable_path = os.path.join(test_build_dir, test_executable_name)

    # Check if the file exists and is not a directory
    if os.path.isfile(test_executable_path):
        final_executable_path = os.path.join(build_dir,
                                             test_executable_name)  # The final location for the test executable
        if os.path.exists(final_executable_path):
            os.rmdir(final_executable_path)  # Remove it if it already exists
        os.rename(test_executable_path, final_executable_path)
    else:
        logging.error(f"Expected test executable not found: {test_executable_path}")
        sys.exit(1)

def run_tests(build_dir):
    """Run all Google Test unit tests."""
    test_executable = os.path.join(build_dir, 'tests')  # The final location for the test executable
    if not os.path.isfile(test_executable):
        logging.error(f"Test executable not found: {test_executable}")
        sys.exit(1)

    run_command([test_executable], build_dir)

def main():
    if len(sys.argv) != 3:
        logging.error("Usage: python3 run_tests.py <tests_dir> <build_dir>")
        sys.exit(1)

    tests_dir = sys.argv[1]
    build_dir = sys.argv[2]

    if not os.path.isdir(tests_dir):
        logging.error(f"Tests directory does not exist: {tests_dir}")
        sys.exit(1)

    compile_tests(tests_dir, build_dir)
    run_tests(build_dir)

if __name__ == "__main__":
    main()
