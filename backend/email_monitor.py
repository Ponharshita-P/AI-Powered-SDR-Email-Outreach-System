import imaplib
import email
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

FROM_EMAIL = os.getenv("FROM_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# IMAP Server Settings
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# SMTP Server Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_reply_email(msg_id, from_address, subject):

    if any(value is None for value in [msg_id, from_address, subject]):
        print("Invalid. Please provide proper data!")
        return None

    # Set up the email headers
    reply_subject = f"Re: {subject}"
    to_address = from_address
    from_address = FROM_EMAIL

    reply_content = f"Hi,\n\nThank you for your response! We will get back to you shortly.\n\nBest Regards,\nCloud Solutions Inc."

    msg = MIMEText(reply_content, 'plain', 'utf-8')
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = reply_subject
    msg['In-Reply-To'] = msg_id
    msg['References'] = msg_id

    # Send the reply email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            connection.login(from_address, APP_PASSWORD)
            connection.sendmail(from_address, to_address, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error in sending email: {e}")


def check_for_replies(FROM_EMAIL, APP_PASSWORD):
    message_id, subject, from_address = None, None, None
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(FROM_EMAIL, APP_PASSWORD)

        mail.select("inbox")
        # Search for unread emails or emails that contain "Re:" in the subject
        status, messages = mail.search(None, '(UNSEEN)')

        if status == "OK":
            for num in messages[0].split():
                status, msg_data = mail.fetch(num, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Get required headers from the original email
                message_id = msg['Message-ID']
                subject = msg['Subject']
                from_address = msg['From']

        print(message_id, subject, from_address) 
        return message_id, subject, from_address

    except Exception as e:
        raise Exception(f"Error in checking the responses: {e}")
    

def check_mails_and_reply():
    message_id, subject, from_address = check_for_replies(FROM_EMAIL, APP_PASSWORD)
    send_reply_email(message_id, from_address, subject)

    
#if __name__ == "__main__":
#    check_mails_and_reply()