#!/bin/sh

if [ "$KAFKA_SERVICE" = "kafka" ]
then
    echo "Waiting for Kafka ..."

    while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
      sleep 10
    done

    echo "Kafka started"
fi

if [ "$RABBITMQ_SERVICE" = "rabbit" ]
then
    echo "Waiting for RabbitMQ ..."

    while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
      sleep 10
    done

    echo "RabbitMQ started"
fi

exec "$@"