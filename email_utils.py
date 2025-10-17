# email_utils.py
import smtplib
from email.message import EmailMessage
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(to_address: str, subject: str, body: str) -> bool:
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.set_content(body)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False
