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

    # Move the test executable to the build directory if it is not already there
    test_executable = os.path.join(test_build_dir, 'tests')  # Adjust if your executable is named differently
    final_executable_path = os.path.join(build_dir, 'tests')  # The final location for the test executable
    if os.path.isfile(test_executable) and not os.path.isfile(final_executable_path):
        os.rename(test_executable, final_executable_path)

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
