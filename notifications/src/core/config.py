import os
from logging import config as logging_config

from notifications.src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)

KAFKA_TOPICS = {
    'registration': {
        'group_id': 'registration',
    },
    'weekly_reminder': {
        'group_id': 'weekly-reminder',
    },
    'monthly_statistic': {
        'group_id': 'monthly-statistic',
    },
}

EMAIL_TEMPLATES = {
    'send_greeting': 'send_greeting.html',
    'send_reminder': 'send_reminder.html',
    'send_statistic': 'send_statistic.html',
}

QUEUE = {
    'send_greeting': 'urgent_queue',
    'send_reminder': 'common_queue',
    'send_statistic': 'common_queue',
}

KAFKA_HOST = os.getenv('KAFKA_HOST', '127.0.0.1')
KAFKA_PORT = int(os.getenv('KAFKA_PORT', 9092))
KAFKA_URL = f'{KAFKA_HOST}:{KAFKA_PORT}'

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PWD = os.getenv('RABBITMQ_PWD', 'guest')
RABBITMQ_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PWD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'
