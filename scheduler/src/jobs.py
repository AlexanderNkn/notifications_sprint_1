"""Scheduled jobs."""

import json
import logging
import time

import backoff  # type: ignore
import kafka  # type: ignore
import schedule  # type: ignore
from kafka import KafkaProducer

from scheduler.src.config import KAFKA_URL

schedule_logger = logging.getLogger('schedule')


@backoff.on_exception(backoff.expo, kafka.errors.KafkaError, max_time=120)
def get_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=[KAFKA_URL],
        value_serializer=lambda msg: json.dumps(msg).encode('ascii'),
    )


def send_greeting() -> None:
    producer = get_producer()
    schedule_logger.info('Sending registration event')
    producer.send('registration', {'event': 'send_greeting'})
    schedule_logger.info('Registration event successfully sent')
    time.sleep(1)
    producer.close()


def send_weekly_reminder() -> None:
    producer = get_producer()
    schedule_logger.info('Sending weekly_reminder event')
    producer.send('weekly_reminder', {'event': 'send_reminder'})
    schedule_logger.info('Weekly_reminder event successfully sent')
    time.sleep(1)
    producer.close()


def send_monthly_statistic() -> None:
    producer = get_producer()
    schedule_logger.info('Sending monthly_statistic event')
    producer.send('monthly_statistic', {'event': 'send_statistic'})
    schedule_logger.info('Monthly_statistic event successfully sent')
    time.sleep(1)
    producer.close()


def test_sending_events() -> None:
    """Send all events to Kafka at once for testing purpose."""
    send_greeting()
    send_weekly_reminder()
    send_monthly_statistic()
    return schedule.CancelJob
