FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/code

COPY ["email/requirements.txt", "email/docker/rabbit_mailhog_waiter.sh", "./"]

RUN apt update && apt install -y netcat \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/* \
    && chmod +x /usr/src/code/rabbit_mailhog_waiter.sh

ENTRYPOINT ["/usr/src/code/rabbit_mailhog_waiter.sh"]

COPY ["./email", "./"]

CMD ["python", "src/worker.py"]

