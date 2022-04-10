"""Mapping events with their methods."""
from notifications.utils import (
    get_data_for_greeting_letter,
    get_data_for_monthly_statistics,
    get_data_for_weekly_reminder,
)

KAFKA_TOPICS = {
    'registration': {
        'group_id': 'registration',
    },
    'weekly_reminder': {
        'group_id': 'weekly-reminder',
    },
    'monthly_statistic': {
        'group_id': 'monthly-statistic',
    },
}

EVENT_HANDLERS = {
    'send_greeting': get_data_for_greeting_letter,
    'send_reminder': get_data_for_weekly_reminder,
    'send_statistic': get_data_for_monthly_statistics,
}

EMAIL_TEMPLATES = {
    'send_greeting': 'send_greeting.html',
    'send_reminder': 'send_reminder.html',
    'send_statistic': 'send_statistic.html',
}

QUEUE = {
    'send_greeting': 'urgent_queue',
    'send_reminder': 'common_queue',
    'send_statistic': 'common_queue',
}
