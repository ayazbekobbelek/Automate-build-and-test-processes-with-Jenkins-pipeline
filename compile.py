import subprocess
import logging
import sys
import os
from zipfile import ZipFile
from cryptography.fernet import Fernet


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def run_command(command, working_dir):
    """
    Run a system command in the given working directory and log the output.
    """
    logging.info(f"Running command: {' '.join(command)} in directory {working_dir}")
    try:
        output = subprocess.check_output(command, cwd=working_dir, stderr=subprocess.STDOUT)
        logging.info(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{' '.join(command)}' failed with return code {e.returncode}")
        logging.error(e.output.decode('utf-8'))
        sys.exit(e.returncode)


def compile_code(source_dir, build_dir):
    """
    Compile the code using CMake and GCC in the build directory.
    """
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    # Run CMake to configure the project
    run_command(['cmake', source_dir], build_dir)

    # Build the project
    run_command(['cmake', '--build', build_dir], build_dir)


def encrypt_file(file_path, key):
    """
    Encrypt a file using Fernet symmetric encryption.
    """
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(file_path + ".enc", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    logging.info(f"File {file_path} encrypted.")


def compress_files(build_dir):
    """
    Compress the contents of the build directory into a zip file.
    """
    zip_filename = os.path.join(build_dir, "build_artifacts.zip")
    with ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, build_dir))
    logging.info(f"Build directory {build_dir} compressed into {zip_filename}.")



def main():
    if len(sys.argv) < 3:
        logging.error("Usage: python compile.py <source_directory> <build_directory> [--encrypt] [--compress]")
        sys.exit(1)

    source_directory = sys.argv[1]
    build_directory = sys.argv[2]
    should_encrypt = '--encrypt' in sys.argv
    should_compress = '--compress' in sys.argv

    compile_code(source_directory, build_directory)

    key = Fernet.generate_key()
    fernet = Fernet(key)

    # If encryption is needed
    if should_encrypt:
        for root, dirs, files in os.walk(build_directory):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path) and not file_path.endswith('.enc'):
                    encrypt_file(file_path, key)

    # Compression step
    if should_compress:
        compress_files(build_directory)

    # You can output the key to a file or pass it securely to whoever needs to decrypt the files
    with open('encryption.key', 'wb') as keyfile:
        keyfile.write(key)

    logging.info("Compilation and packaging completed.")

if __name__ == "__main__":
    main()
