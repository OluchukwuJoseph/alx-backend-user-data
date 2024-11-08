#!/usr/bin/env python3
""" This script contains the `filter_datum` function """
from typing import List
import re
import logging


def filter_datum(fields: List, redaction: str, message: str, seperator: str):
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
        message = filter_datum(self.fields, self.REDACTION, record.msg, ';')
        record.msg = message
        return super(RedactingFormatter, self).format(record)