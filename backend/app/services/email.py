import os
import logging
import resend

logger = logging.getLogger(__name__)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM", "PulseOps <alerts@example.com>")

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

def send_transactional_email(to_email: str, subject: str, html_content: str):
    if not RESEND_API_KEY:
        logger.warning(f"RESEND_API_KEY is not configured. Skipping email to {to_email}")
        return False

    try:
        response = resend.Emails.send({
            "from": EMAIL_FROM,
            "to": to_email,
            "subject": subject,
            "html": html_content
        })
        logger.info(f"Email sent successfully to {to_email}. Resend ID: {response.get('id')}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise
