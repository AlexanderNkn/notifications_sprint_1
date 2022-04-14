import os
from logging import config as logging_config

from .logger import LOGGING

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

QUEUE = {
    'send_greeting': {
        'exchange': 'test-exchange',
        'routing_key': '_user-reporting.v1.registered_',
    },
    'send_reminder': {
        'exchange': 'test-exchange',
        'routing_key': '_admin-panel.v1.active-users_',
    },
    'send_statistic': {
        'exchange': 'test-exchange',
        'routing_key': '_admin-panel.v1.monthly_statistic_',
    },
    # TODO add sms notifications
    'send_statistic_sms': {
        'exchange': 'test-exchange',
        'routing_key': '_sms.monthly_statistic_',
    },
}

KAFKA_HOST = os.getenv('KAFKA_HOST', '127.0.0.1')
KAFKA_PORT = int(os.getenv('KAFKA_PORT', 9092))
KAFKA_URL = f'{KAFKA_HOST}:{KAFKA_PORT}'

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PWD = os.getenv('RABBITMQ_PWD', 'guest')
RABBITMQ_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PWD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}'
