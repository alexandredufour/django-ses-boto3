import threading
import boto3
import botocore.exceptions

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address


class SESEmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super(SESEmailBackend, self).__init__(*args, **kwargs)
        self.connection = None
        self._lock = threading.RLock()

    def open(self):
        if self.connection:
            return False
        ses_region_name = settings.AWS_SES_REGION_NAME or 'us-west-2'
        self.connection = boto3.client('ses', region_name=ses_region_name)
        return True

    def close(self):
        self.connection = None

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return
        with self._lock:
            new_conn_created = self.open()
            if not self.connection:
                # We failed silently on open().
                # Trying to send would be pointless.
                return
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
            if new_conn_created:
                self.close()
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = sanitize_address(email_message.from_email, encoding)
        recipients = [sanitize_address(addr, encoding) for addr in email_message.recipients()]
        message = email_message.message()
        try:
            self.connection.send_raw_email(
                Source=from_email,
                Destinations=recipients,
                RawMessage={
                    'Data': message.as_bytes(linesep='\r\n')
                }
            )
        except botocore.exceptions.ClientError:
            if not self.fail_silently:
                raise
            return False
        return True
