"""Module containes methods for gathering data from other services for notifications."""
import json
from collections.abc import Callable
from typing import Generator


def get_handler(event: str) -> Callable[..., Generator[dict, None, None]] | None:
    """Mapps event with its method to fetch data for current event."""
    return {
        'send_greeting': get_data_for_greeting_letter,
        'send_reminder': get_data_for_weekly_reminder,
        'send_statistic': get_data_for_monthly_statistics,
    }.get(event)


def get_fake_data(file_path) -> dict:
    with open(file_path) as feed:
        return json.load(feed)


def get_data_for_greeting_letter(**kwargs) -> Generator[dict, None, None]:
    # TODO fetch data from auth service and transform it.
    # Due to auth service is unavailable in sprint10 only mock data will be returned.
    collected_data = get_fake_data('notifications/examples/welcome.json')
    for notification_data in collected_data['welcome']:
        yield notification_data


def get_data_for_weekly_reminder(**kwargs) -> Generator[dict, None, None]:
    # TODO fetch data from auth and movie-api services and transform it.
    # Due to auth and movie-api services are unavailable in sprint10 only mock data will be returned.
    collected_data = get_fake_data('notifications/examples/weekly_reminder.json')
    for notification_data in collected_data['weekly_reminder']:
        yield notification_data


def get_data_for_monthly_statistics(**kwargs) -> Generator[dict, None, None]:
    # TODO fetch data from auth, ugc and movie-api services and transform it.
    # Due to auth, ugc and movie-api services are unavailable in sprint10 only mock data will be returned.
    collected_data = get_fake_data('notifications/examples/monthly_statistic.json')
    for notification_data in collected_data['montly_statistic']:
        yield notification_data
