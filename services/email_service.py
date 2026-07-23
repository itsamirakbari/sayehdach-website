import logging
import mimetypes
import smtplib

from email.message import EmailMessage
from email.utils import formataddr

from config import Config


logger = logging.getLogger(__name__)


SMTP_TIMEOUT = 10


def send_contact_email(
    name,
    email,
    phone,
    subject,
    message,
    attachments,
):
    """
    Send contact form email with optional attachments.

    Args:
        name (str): Customer name.
        email (str): Customer email address.
        phone (str): Customer phone number.
        subject (str): Email subject.
        message (str): Customer message.
        attachments (list): Uploaded files.

    Returns:
        bool: True if email was sent successfully, otherwise False.
    """

    try:
        logger.info("Preparing contact email from %s", name)

        email_message = EmailMessage()

        email_message["Subject"] = subject
        email_message["From"] = formataddr(
            ("SAYEHDACH Website", Config.MAIL_USERNAME)
        )
        email_message["To"] = Config.MAIL_RECEIVER
        email_message["Reply-To"] = email

        plain_text = f"""
Neue Kontaktanfrage über die SAYEHDACH Website

Name:
{name}

E-Mail:
{email}

Telefon:
{phone}

Nachricht:
{message}
"""

        html_content = f"""
<html>
    <body>
        <h2>Neue Kontaktanfrage</h2>
        <p><strong>Name:</strong><br>{name}</p>
        <p><strong>E-Mail:</strong><br>{email}</p>
        <p><strong>Telefon:</strong><br>{phone}</p>
        <p><strong>Nachricht:</strong><br>{message}</p>
        <hr>
        <p>SAYEHDACH Website Anfrage</p>
    </body>
</html>
"""

        email_message.set_content(plain_text)
        email_message.add_alternative(
            html_content,
            subtype="html",
        )

        for file in attachments:
            if not file or not file.filename:
                continue

            mime_type, _ = mimetypes.guess_type(file.filename)

            if mime_type is None:
                mime_type = "application/octet-stream"

            main_type, sub_type = mime_type.split("/", 1)

            email_message.add_attachment(
                file.read(),
                maintype=main_type,
                subtype=sub_type,
                filename=file.filename,
            )

            logger.info("Attachment added: %s", file.filename)

        with smtplib.SMTP(
            Config.MAIL_SERVER,
            Config.MAIL_PORT,
            timeout=SMTP_TIMEOUT,
        ) as server:
            if Config.MAIL_USE_TLS:
                server.starttls()

            server.login(
                Config.MAIL_USERNAME,
                Config.MAIL_PASSWORD,
            )

            server.send_message(email_message)

        logger.info("Contact email sent successfully")

        return True

    except Exception:
        logger.exception("Failed to send contact email")
        return False
