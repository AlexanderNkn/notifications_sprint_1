"""Module containes methods for gathering data from other services for notifications."""
from collections.abc import Callable


def get_handler(event: str) -> Callable[..., dict] | None:
    """Mapping event with its method to fetch data for current event."""
    return {
        'send_greeting': get_data_for_greeting_letter,
        'send_reminder': get_data_for_weekly_reminder,
        'send_statistic': get_data_for_monthly_statistics,
    }.get(event)


def get_data_for_greeting_letter(**kwargs) -> dict:
    # TODO fetch data from auth service and transform it.
    # Due to auth service is unavailable in sprint10 only mock data will be returned.
    return kwargs


def get_data_for_weekly_reminder(**kwargs) -> dict:
    # TODO fetch data from auth and movie-api services and transform it.
    # Due to auth and movie-api services are unavailable in sprint10 only mock data will be returned.
    return kwargs


def get_data_for_monthly_statistics(**kwargs) -> dict:
    # TODO fetch data from auth, ugc and movie-api services and transform it.
    # Due to auth, ugc and movie-api services are unavailable in sprint10 only mock data will be returned.
    return kwargs
