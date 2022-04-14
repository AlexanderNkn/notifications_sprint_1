import json
import logging

import pika  # type: ignore

from core import config
from sender.message_render import get_message
from sender.smtplib_sender import SMTPLibSender

logger = logging.getLogger('email_notification')


def send_mail_with_template(channel, method_frame, header_frame, body, subject, template_path):
    msg_body = json.loads(body)
    recipient = msg_body.get('email')
    message = get_message(template_path, msg_body)
    sender.send([recipient], message, config.EMAIL_USER, subject)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def send_welcome_mail(channel, method_frame, header_frame, body):
    send_mail_with_template(channel, method_frame, header_frame, body, 'Привет!', 'templates/welcome.html')


def send_weekly_reminder_mail(channel, method_frame, header_frame, body):
    send_mail_with_template(channel, method_frame, header_frame, body, 'Привет!', 'templates/weekly_reminder.html')


def send_monthly_statistic_mail(channel, method_frame, header_frame, body):
    send_mail_with_template(channel, method_frame, header_frame, body, 'Привет!', 'templates/monthly_statistic.html')


credentials = pika.PlainCredentials(config.RABBITMQ_USER, config.RABBITMQ_PWD)
parameters = pika.ConnectionParameters(host=config.RABBITMQ_HOST, port=config.RABBITMQ_PORT, credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.basic_qos(prefetch_count=1)
channel.basic_consume('_emails.send-welcome_', send_welcome_mail)
channel.basic_consume('_emails.send-weekly-reminder_', send_weekly_reminder_mail)
channel.basic_consume('_emails.send-monthly-statistic_', send_monthly_statistic_mail)

sender = SMTPLibSender()

if __name__ == '__main__':
    sender.connect(config.EMAIL_SERVER, config.EMAIL_PORT, config.EMAIL_USER, config.EMAIL_PWD, config.EMAIL_SSL)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()
    sender.disconnect()
