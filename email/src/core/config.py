import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'email_notification')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PWD = os.getenv('RABBITMQ_PWD', 'guest')

EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PWD = os.getenv('EMAIL_PWD', '')
EMAIL_SERVER = os.getenv('EMAIL_SERVER', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '465'))
email_ssl = os.getenv('EMAIL_SSL')
if email_ssl and email_ssl.lower() == 'true':
    EMAIL_SSL = True
else:
    EMAIL_SSL = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
