#!/bin/sh

if [ "$EMAIL_SERVER" = "mailhog" ]
then
    echo "Waiting for Mailhog ..."

    while ! nc -z $EMAIL_SERVER $EMAIL_PORT; do
      sleep 10
    done

    echo "Mailhog started"
fi

if [ "$RABBITMQ_HOST" = "rabbit" ]
then
    echo "Waiting for RabbitMQ ..."

    while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
      sleep 10
    done

    echo "RabbitMQ started"
fi

exec "$@"
