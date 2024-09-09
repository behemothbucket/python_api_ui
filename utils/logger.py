import json
import logging

from prettytable import PrettyTable


class CustomFilter(logging.Filter):
    COLOR = {
        "DEBUG": "GREEN",
        "INFO": "GREEN",
        "WARNING": "YELLOW",
        "ERROR": "RED",
        "CRITICAL": "RED",
    }

    def filter(self, record):
        record.color = CustomFilter.COLOR[record.levelname]
        return True


logger = logging.getLogger("Logger")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s]: %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.addFilter(CustomFilter())


def log_response(method, url, payload=None, response=None):
    log_message = f'\n{method} {url}'

    if payload:
        if hasattr(payload, 'model_dump_json'):
            payload_str = payload.model_dump_json(indent=4).encode("utf-8").decode("utf-8")
        else:
            payload_str = json.dumps(payload, indent=4).encode().decode("unicode-escape")

        log_message += f'\nPayload: {payload_str}'

    if response:
        response_str = json.dumps(response, indent=4).encode().decode("unicode-escape")
        log_message += f'\nResponse: {response_str}'

    logger.info(log_message)


def log_run_output(field_names: list[str], rows: list[list[str]]):
    table = PrettyTable()
    table.field_names = field_names
    table.add_rows(rows)
    logger.info(f'\n{table.get_string()}')
