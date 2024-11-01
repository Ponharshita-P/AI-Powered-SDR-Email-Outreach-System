import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

FROM_ADDRESS = os.getenv("FROM_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# SMTP Server Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(subject: str, to_address: str, email_content_text: str):
    msg = MIMEText(email_content_text, 'plain', 'utf-8')
    msg['From'] = FROM_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            connection.login(FROM_ADDRESS, APP_PASSWORD)
            connection.sendmail(FROM_ADDRESS, to_address, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error in sending email: {e}")