import subprocess
import logging
import smtplib
from email.message import EmailMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def send_email(subject, content, recipient_emails):
    # Create the email message
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = 'no-reply@localhost'
    msg['To'] = ', '.join(recipient_emails)

    # Connect to the local SMTP server
    with smtplib.SMTP('localhost', 1025) as server:
        # Send the email
        server.send_message(msg)
        logging.info(f"Email sent to {', '.join(recipient_emails)}")


def main():
    # Call the compile.py script and capture the exit status
    compile_command = ['python', 'compile.py', 'source_dir', 'build_dir', '--encrypt', '--compress']
    status = subprocess.call(compile_command)

    subject = "Build Status"
    if status == 0:
        content = "The build completed successfully."
    else:
        content = "The build failed. Please check the logs for more information."
    recipient_emails = ['developer@example.com', 'qa@example.com']  # Add your recipients here

    send_email(subject, content, recipient_emails)


if __name__ == "__main__":
    main()
