#!/usr/bin/env python3
""" This script contains the `filter_datum` function """
from typing import List, Tuple, Union
import re
import logging


def filter_datum(fields: Union[List, Tuple], redaction: str,
                 message: str, seperator: str) -> str:
    """ Returns the log message obfuscated """
    new_message = re.sub(rf'({"|".join(fields)})=[^{seperator}]+',
                         rf'\1={redaction}', message)
    return new_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPERATOR = ';'

    def __init__(self, **kwargs):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        if 'fields' in kwargs:
            self.fields = kwargs['fields']

    def format(self, record: logging.LogRecord) -> str:
        message = filter_datum(self.fields, self.REDACTION,
                               record.msg, self.SEPERATOR)
        record.msg = message
        return super(RedactingFormatter, self).format(record)


class CustomFilter():
    def __init__(self, level: int):
        self.max_level = level

    def filter(self, record: logging.LogRecord):
        return record.levelno <= self.max_level


PII_FIELDS = ('ssn', 'password', 'ip', 'email', 'phone')


def get_logger() -> logging.Logger:
    """ Returns a Logger object """
    new_logger = logging.getLogger('user_data')
    new_logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    console_handler.addFilter(CustomFilter(logging.INFO))
    new_logger.addHandler(console_handler)

    return new_logger
