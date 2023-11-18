import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import argparse

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def service_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/belekayazbekov/Downloads/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def send_email(subject, content, recipient_emails, attachment_path=None):
    service = service_gmail()

    # Create a message
    message = MIMEMultipart()
    message['to'] = ', '.join(recipient_emails)
    message['subject'] = subject
    msg = MIMEText(content)
    message.attach(msg)

    # Attach the file if provided
    if attachment_path and os.path.isfile(attachment_path):
        with open(attachment_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
        message.attach(part)

    # Send the message
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}
    service.users().messages().send(userId='me', body=body).execute()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Send an email using Gmail API.')
    parser.add_argument('subject', help='The subject of the email')
    parser.add_argument('body', help='The body content of the email')
    parser.add_argument('recipient', help='Email recipient')
    parser.add_argument('--attachment', help='Path to attachment file', default=None)
    return parser.parse_args()

def main():
    args = parse_arguments()

    subject = args.subject
    content = args.body
    recipient_emails = [args.recipient]  # Assumes a single recipient, modify as needed
    attachment_path = args.attachment

    send_email(subject, content, recipient_emails, attachment_path)


if __name__ == '__main__':
    main()
