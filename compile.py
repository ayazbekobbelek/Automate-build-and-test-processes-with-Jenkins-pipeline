# compile.py

import subprocess
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def run_command(command, working_dir):
    """
    Run a shell command in the specified directory and return its output.
    """
    try:
        logging.info("Running command: %s in directory %s", ' '.join(command), working_dir)
        output = subprocess.check_output(command, cwd=working_dir)
        decoded_output = output.decode('utf-8').strip()
        logging.info("Command output:\n%s", decoded_output)  # Log the command output
        return decoded_output
    except subprocess.CalledProcessError as e:
        logging.error("Error while running command: %s", e)
        return None


def compile_code(source_dir, build_dir):
    """
    Use CMake to configure and compile C code.
    """
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    # Configure with CMake
    cmake_configure_result = run_command(['cmake', source_dir], build_dir)
    if cmake_configure_result is None:
        return

    # Build with CMake (invokes the build system, e.g., make or ninja)
    cmake_build_result = run_command(['cmake', '--build', '.'], build_dir)
    if cmake_build_result is None:
        return


def main():
    if len(sys.argv) != 3:
        logging.error("Usage: compile.py [path_to_source_directory] [path_to_build_directory]")
        sys.exit(1)

    source_directory = sys.argv[1]
    build_directory = sys.argv[2]

    compile_code(source_directory, build_directory)


if __name__ == "__main__":
    main()
