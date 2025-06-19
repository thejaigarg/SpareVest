# app/core/email.py

import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
import aiosmtplib

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("GMAIL_USER")
SMTP_PASS = os.getenv("GMAIL_PASS")

async def send_reset_email(to_email: str, reset_link: str):
    subject = "Your Password Reset Link"
    body = f"""Hi,
Click this link to reset your password: {reset_link}
If you did not request this, you can safely ignore this email.
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    await aiosmtplib.send(
        msg,
        hostname=SMTP_SERVER,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USER,
        password=SMTP_PASS,
    )