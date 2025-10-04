"""
Custom Email Backend using Resend API
"""
import resend
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


class ResendBackend(BaseEmailBackend):
    """
    Email backend that uses Resend API to send emails
    """

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        resend.api_key = settings.RESEND_API_KEY

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        if not email_messages:
            return 0

        num_sent = 0
        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1
        return num_sent

    def _send(self, email_message):
        """Send a single email message"""
        try:
            # Prepare email data
            params = {
                "from": email_message.from_email or settings.DEFAULT_FROM_EMAIL,
                "to": email_message.to,
                "subject": email_message.subject,
            }

            # Add HTML content if available
            if hasattr(email_message, 'alternatives') and email_message.alternatives:
                for content, mimetype in email_message.alternatives:
                    if mimetype == 'text/html':
                        params["html"] = content
                        break

            # Fallback to plain text
            if "html" not in params and email_message.body:
                params["html"] = email_message.body.replace('\n', '<br>')

            # Add CC if present
            if email_message.cc:
                params["cc"] = email_message.cc

            # Add BCC if present
            if email_message.bcc:
                params["bcc"] = email_message.bcc

            # Add Reply-To if present
            if email_message.reply_to:
                params["reply_to"] = email_message.reply_to

            # Send email via Resend
            response = resend.Emails.send(params)

            return True

        except Exception as e:
            if not self.fail_silently:
                raise
            return False