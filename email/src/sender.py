import logging
import os
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

from core import config

logger = logging.getLogger('email_notification')

template_dir = os.path.dirname(os.path.dirname(__file__))


def send_mail(recepient: str, template_path: str, msg_data: dict, subject=None) -> None:

    sender = config.EMAIL_USER
    password = config.EMAIL_PWD
    smtpStr = config.EMAIL_SERVER
    smtpPort = config.EMAIL_PORT

    smtp_serv = smtplib.SMTP(smtpStr, smtpPort)
    smtp_serv.login(sender, password)

    message = EmailMessage()
    message["From"] = sender
    message["To"] = ",".join([recepient])
    message["Subject"] = subject

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_path)
    output = template.render(**msg_data)

    message.add_alternative(output, subtype='html')

    try:
        smtp_serv.sendmail(sender, [recepient], message.as_string())
    except smtplib.SMTPException:
        logger.exception('cannot send email')

    smtp_serv.close()
