import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")  # Now using Amazon's SES default

def send_email_notification(to_email, subject, message):
    """Sends an email notification using Amazon SES."""
    try:
        # Create email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM  # Now using Amazon's default domain
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Connect to SES SMTP server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()  # Upgrade to secure TLS connection
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"Email failed: {e}")
        return False
