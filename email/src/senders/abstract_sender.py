from abc import ABC, abstractmethod


class AbstractEmailSender(ABC):
    """Abstract class for remote storage."""

    def __init__(self):
        pass

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def send(self, recipients: list[str], message: str, *args, **kwargs):
        pass

    @abstractmethod
    def disconnect(self, *args, **kwargs):
        pass
