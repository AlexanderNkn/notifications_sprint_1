"""
Main process.

The script manages consuming events from event bus, gathering related data and transfering
data to rabbitmq queue for further sending notifications to users.
"""
import json
from multiprocessing import Process

import pika
from kafka import KafkaConsumer

from notifications.handlers import EMAIL_TEMPLATES, EVENT_HANDLERS, KAFKA_TOPICS, QUEUE


def process_event(topic: str) -> None:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id=KAFKA_TOPICS[topic]['group_id'],
        value_deserializer=lambda msg: json.loads(msg.decode('ascii')),
    )

    for message in consumer:
        event = message.value.pop('event')
        if data_for_notification := get_notification_data(event, **message.value):
            send_data_to_queue(event, data_for_notification)


def get_notification_data(event: str, **kwargs) -> dict | None:
    if handler := EVENT_HANDLERS.get(event):
        return handler(**kwargs)


def send_data_to_queue(event: str, data) -> None:
    params = pika.URLParameters(url='amqp://guest:guest@localhost:5672')
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
