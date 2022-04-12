"""
Main process.

The script manages consuming events from event bus, gathering related data and transfering
data to rabbitmq queue for further sending notifications to users.
"""
import json
from multiprocessing import Process

import pika  # type: ignore
from kafka import KafkaConsumer  # type: ignore
from notifications.src.core.config import EMAIL_TEMPLATES, KAFKA_TOPICS, KAFKA_URL, QUEUE, RABBITMQ_URL
from notifications.src.core.handlers import get_handler


def process_event(topic: str) -> None:
    """Manages consuming data from event bus and related services then sending to rabbitmq queue."""
    consumer: KafkaConsumer = get_consumer(topic)
    
    for message in consumer:
        event = message.value.pop('event')
        if data_for_notification := get_notification_data(event, **message.value):
            send_data_to_queue(event, data_for_notification)
        consumer.commit()


def get_consumer(topic: str) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=[KAFKA_URL],
        auto_offset_reset='earliest',
        group_id=KAFKA_TOPICS[topic]['group_id'],
        value_deserializer=lambda msg: json.loads(msg.decode('ascii')),
    )


def get_notification_data(event: str, **kwargs) -> dict | None:
    """Collects data related to specific event from related services."""
    if handler := get_handler(event):
        return handler(**kwargs)
    return None


def send_data_to_queue(event: str, data) -> None:
    """Sends prepared data to rabbitmq queue."""
    params = pika.URLParameters(url=RABBITMQ_URL)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE[event], durable=True)

    data.update({'template': EMAIL_TEMPLATES[event]})
    channel.basic_publish(exchange='', routing_key=QUEUE[event], body=json.dumps(data))
    connection.close()


if __name__ == '__main__':
    for topic in KAFKA_TOPICS:
        process = Process(target=process_event, args=(topic,))
        process.start()
