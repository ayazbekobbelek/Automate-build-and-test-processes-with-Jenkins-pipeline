import argparse
import subprocess
import logging
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
        raise


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


def encrypt_file(file_path, key, encrypted_dir):
    """
    Encrypt a file using Fernet symmetric encryption and store it in a separate directory.
    """
    # Ensure the encrypted_dir exists
    os.makedirs(encrypted_dir, exist_ok=True)

    # Determine the path for the encrypted file
    encrypted_file_path = os.path.join(encrypted_dir, os.path.basename(file_path) + ".enc")

    # Encrypt and write the file
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    logging.info(f"File {file_path} encrypted to {encrypted_file_path}.")


def compress_files(build_dir):
    """
    Compress the contents of the build directory into a zip file using Zip64 for large files.
    """
    zip_filename = os.path.join(build_dir, "build_artifacts.zip")
    with ZipFile(zip_filename, 'w', allowZip64=True) as zipf:
        for root, _, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Add the file to the zip file; specifying the arcname sets the name within the zip file
                zipf.write(file_path, arcname=os.path.relpath(file_path, build_dir))
    logging.info(f"Build directory {build_dir} compressed into {zip_filename}.")


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Compile, encrypt, and compress code.")
    parser.add_argument("source_dir", help="The source directory where the code is located.")
    parser.add_argument("build_dir", help="The build directory where the compiled code will be placed.")
    parser.add_argument("--encrypt", help="Encrypt the compiled files.", action="store_true")
    parser.add_argument("--compress", help="Compress the build directory into a zip file.", action="store_true")
    return parser.parse_args()


def main():
    args = parse_arguments()

    compile_code(args.source_dir, args.build_dir)

    # Encryption and compression
    if args.encrypt or args.compress:
        # Directory to hold encrypted files
        encrypted_dir = os.path.join(args.build_dir, "encrypted")

        key = Fernet.generate_key()

        # If encryption is needed
        if args.encrypt:
            for root, dirs, files in os.walk(args.build_dir):
                # Skip .git or other directories if needed
                if '.git' in dirs:
                    dirs.remove('.git')

                for file in files:
                    file_path = os.path.join(root, file)
                    # Avoid encrypting already encrypted or non-target files
                    if not file_path.startswith(encrypted_dir) and not file_path.endswith('.enc'):
                        encrypt_file(file_path, key, encrypted_dir)

        # Compression step
        if args.compress:
            compress_files(args.build_dir)

        # Save the encryption key if necessary
        if args.encrypt:
            with open(os.path.join(encrypted_dir, 'encryption.key'), 'wb') as keyfile:
                keyfile.write(key)

        logging.info("Compilation and packaging completed.")


if __name__ == "__main__":
    main()
