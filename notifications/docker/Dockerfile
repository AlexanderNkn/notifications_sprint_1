FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["notifications/requirements.txt", "notifications/kafka_rabbit_waiter.sh", "./"]

RUN apt update && apt install -y netcat \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* \
    && chmod +x /usr/src/code/kafka_rabbit_waiter.sh

ENTRYPOINT ["/usr/src/code/kafka_rabbit_waiter.sh"]

COPY ["notifications", "./notifications"]

CMD ["python3", "notifications/src/worker.py"]
