import time
import requests
import logging

from app.core.settings import settings

VALUE_FIELD = "value"
STATUS_FIELD = "ready"

logging.basicConfig(level=logging.DEBUG)


def get_nested_status(response: requests.Response) -> bool:
    status = response.json().get(VALUE_FIELD).get(STATUS_FIELD)
    return status


def wait_for_webdriver(retry_max: int = 10, delay: float = 1) -> bool:
    retry = 0
    status = None
    while not status:
        try:
            response = requests.get(str(settings.GONETS.REMOTE_DRIVER_STATUS))
        except Exception as e:
            logging.error(f"Error: {e}")
        else:
            status = get_nested_status(response)
            logging.info(f"Check availability. Status: {status}, try: {retry}")

        if retry >= retry_max:
            logging.critical("RetryError: connection failed")
            return False

        retry += 1
        time.sleep(delay)

    return True
