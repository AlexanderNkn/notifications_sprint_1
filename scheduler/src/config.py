import os

KAFKA_HOST = os.getenv('KAFKA_HOST', '127.0.0.1')
KAFKA_PORT = int(os.getenv('KAFKA_PORT', 9092))
KAFKA_URL = f'{KAFKA_HOST}:{KAFKA_PORT}'
