"""
Main process.

The script to run jobs periodically.
"""
import logging
from time import sleep

import schedule

from jobs import send_monthly_statistic, send_weekly_reminder, test_sending_events

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.DEBUG)

schedule.every().friday.do(send_weekly_reminder)
# TODO for monthly events every(4).weeks should be replaced with next_run() with calculated datetime
# because of month is not equal 4 weeks.
schedule.every(4).weeks.do(send_monthly_statistic)
# next job runs once with each restart of scheduler container for testing purpose
schedule.every().minute.do(test_sending_events)

if __name__ == '__main__':
    while True:
        try:
            schedule.run_pending()
        except Exception:
            schedule_logger.exception('Something went wrong')
            sleep(5 * 60)
        else:
            sleep(1)
