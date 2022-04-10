"""
Main process.

The script manages consuming events from event bus, gathering related data and transfering
data to rabbitmq queue for further sending notifications to users.
"""
import json
from multiprocessing import Process

from kafka import KafkaConsumer

from notifications.handlers import EMAIL_TEMPLATES, EVENT_HANDLERS, KAFKA_TOPICS


def process_event(topic: str) -> None:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id=KAFKA_TOPICS[topic]['group_id'],
        value_deserializer=lambda msg: json.loads(msg.decode('ascii')),
    )

    for message in consumer:
        data_for_notification = get_notification_data(**message.value)


def get_notification_data(**kwargs) -> dict | None:
    event = kwargs['event']
    if handler := EVENT_HANDLERS.get(event):
        return handler(**kwargs)


if __name__ == '__main__':
    for topic in KAFKA_TOPICS:
        process = Process(target=process_event, args=(topic,))
        process.start()
