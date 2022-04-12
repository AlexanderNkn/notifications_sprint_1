"""
Main process.

The script manages consuming events from event bus, gathering related data and transfering
data to rabbitmq queue for further sending notifications to users.
"""
import json
import logging
from multiprocessing import Process
from time import sleep
from typing import Generator

import backoff  # type: ignore
import kafka  # type: ignore
import pika  # type: ignore
from kafka import KafkaConsumer  # type: ignore

from notifications.src.core.config import KAFKA_TOPICS, KAFKA_URL, QUEUE, RABBITMQ_URL
from notifications.src.core.handlers import get_handler

logger = logging.getLogger('notifications')


@backoff.on_exception(backoff.expo, kafka.errors.KafkaError, max_time=120)
def get_consumer(topic: str) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=[KAFKA_URL],
        auto_offset_reset='earliest',
        group_id=KAFKA_TOPICS[topic]['group_id'],
        value_deserializer=lambda msg: json.loads(msg.decode('ascii')),
    )


@backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError, max_time=120)
def get_producer() -> pika.BlockingConnection:
    params = pika.URLParameters(url=RABBITMQ_URL)
    params.socket_timeout = 5
    return pika.BlockingConnection(params)


def process_event(topic: str) -> None:
    """Manage consuming data from event bus and related services then sending to rabbitmq queue."""
    logger.info(f'Connecting to {topic} topic in Kafka')
    consumer: KafkaConsumer = get_consumer(topic)
    logger.info(f'Connected successfully to {topic} topic in Kafka')

    for message in consumer:
        event = message.value.pop('event')
        logger.info(f'Collecting data for {event} event')
        if data_for_notification := get_notification_data(event, **message.value):
            logger.info(f'Data for {event} event successfully collected')

            logger.info(f'Sending data for {event} event to RabbitMQ queue')
            send_data_to_queue(event, data_for_notification)
            logger.info(f'Data for {event} event successfully sent to RabbitMQ queue')
        consumer.commit()


def get_notification_data(event: str, **kwargs) -> Generator[dict, None, None] | None:
    """Collect data related to specific event from related services."""
    if handler := get_handler(event):
        return handler(**kwargs)
    return None


def send_data_to_queue(event: str, data_for_notification: Generator[dict, None, None]) -> None:
    """Send prepared data to rabbitmq queue."""
    connection = get_producer()
    channel = connection.channel()

    for message_data in data_for_notification:
        channel.basic_publish(
            exchange=QUEUE[event]['exchange'],
            routing_key=QUEUE[event]['routing_key'],
            body=json.dumps(message_data),
        )
    connection.close()


if __name__ == '__main__':
    while True:
        try:
            for topic in KAFKA_TOPICS:
                process = Process(target=process_event, args=(topic,))
                process.start()
        except Exception:
            logger.exception('Something went wrong')
        sleep(5 * 60)
