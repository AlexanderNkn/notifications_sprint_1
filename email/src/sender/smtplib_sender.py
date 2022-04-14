import logging
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader  # type: ignore

from sender.abstract_sender import AbstractEmailSender

logger = logging.getLogger('email_notification')


class SMTPLibSender(AbstractEmailSender):
    def __init__(self):
        super(SMTPLibSender, self).__init__()
        self.smtp_serv = None

    def connect(self, server: str, port: int, user: str, pwd: str, ssl: bool, *args, **kwargs):
        if ssl:
            self.smtp_serv = smtplib.SMTP_SSL(server, port)
        else:
            self.smtp_serv = smtplib.SMTP(server, port)
        self.smtp_serv.login(user, pwd)

    def send(self, recipients: list[str], message: str, sender: str = None, subject: str = None, *args, **kwargs):
        if not self.smtp_serv:
            raise Exception('Server is not connected')

        email_message = EmailMessage()
        email_message['From'] = sender
        email_message['To'] = ','.join(recipients)
        email_message['Subject'] = subject

        email_message.add_alternative(message, subtype='html')

        try:
            self.smtp_serv.sendmail(sender, recipients, email_message.as_string())
        except smtplib.SMTPException:
            logger.exception('cannot send email')

    def disconnect(self, *args, **kwargs):
        if self.smtp_serv:
            self.smtp_serv.close()
            self.smtp_serv = None
