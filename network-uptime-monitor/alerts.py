import requests
import smtplib
import ssl
from email.message import EmailMessage

import config


def send_telegram(message: str) -> None:
    token = getattr(config, "TELEGRAM_BOT_TOKEN", "")
    chat_id = getattr(config, "TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        # ignore errors in alerts to keep monitor running
        pass


def send_email(message: str) -> None:
    enabled = getattr(config, "EMAIL_ENABLED", False)
    if not enabled:
        return

    email_from = config.EMAIL_FROM
    email_to = config.EMAIL_TO
    subject = config.EMAIL_SUBJECT

    smtp_server = config.SMTP_SERVER
    smtp_port = config.SMTP_PORT
    smtp_username = config.SMTP_USERNAME
    smtp_password = config.SMTP_PASSWORD

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_from
    msg["To"] = email_to
    msg.set_content(message)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    except Exception:
        # ignore errors in alerts to keep monitor running
        pass


def send_alert(message: str) -> None:
    send_telegram(message)
    send_email(message)
