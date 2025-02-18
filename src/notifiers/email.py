import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import logging
from .base import BaseNotifier
import os

class EmailNotifier(BaseNotifier):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.smtp_server = config["smtp_server"]
        self.smtp_port = config["smtp_port"]
        self.sender_email = config["sender_email"]
        self.recipients = config["recipients"]

    def notify(self, publications: List[Dict[str, Any]]) -> bool:
        if not publications:
            return True

        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = ", ".join(self.recipients)
            message["Subject"] = f"New Publications Found ({len(publications)})"

            # Create email body
            body = "The following new publications have been found:\n\n"
            for pub in publications:
                body += f"- {pub['title']} by {pub['publisher']}\n"
                body += f"  Published on: {pub['date']}\n"
                body += f"  Pages: {pub['page_count']}\n"
                body += f"  URL: {pub['url']}\n\n"

            message.attach(MIMEText(body, "plain"))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, os.environ["EMAIL_PASSWORD"])
                server.send_message(message)

            return True

        except Exception as e:
            logging.error(f"Error sending email notification: {str(e)}")
            return False
