#!/usr/bin/env python3
"""
This script contains functions and classes
for logging user data Redactingly
"""
from typing import List, Tuple, Union, Dict
import re
import logging
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """ Returns the log message obfuscated """
    new_message: str = re.sub(rf'({"|".join(fields)})=[^{seperator}]+',
                              rf'\1={redaction}', message)
    return new_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION: str = "***"
    FORMAT: str = "[HOLBERTON] %(name)s %(levelname)s "\
        "%(asctime)-15s: %(message)s"
    SEPERATOR: str = ';'

    def __init__(self, **kwargs: Dict) -> None:
        """ Initializies instance """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        if 'fields' in kwargs:
            self.fields = kwargs['fields']

    def format(self, record: logging.LogRecord) -> str:
        """ Return formatted log record """
        message = filter_datum(self.fields, self.REDACTION,
                               record.msg, self.SEPERATOR)
        record.msg = message
        return super(RedactingFormatter, self).format(record)


class CustomFilter():
    """ Custom Filter class that only logs up to logging.INFO level """
    def __init__(self, level: int) -> None:
        """ Initializies instance """
        self.max_level = level

    def filter(self, record: logging.LogRecord) -> bool:
        """ Return True if log record level is logging.INFO level or below """
        return record.levelno <= self.max_level


PII_FIELDS: Tuple = ('name', 'ssn', 'password', 'email', 'phone')


def get_logger() -> logging.Logger:
    """ Returns a Logger object """
    new_logger: logging.Logger = logging.getLogger('user_data')
    new_logger.setLevel(logging.DEBUG)
    console_handler: logging.Handler = logging.StreamHandler()
    console_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    console_handler.addFilter(CustomFilter(logging.INFO))
    new_logger.addHandler(console_handler)

    return new_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to a database whose credenials
    was provided through environment variables
    """
    DB_USERNAME: str = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    DB_PASSWORD: str = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    DB_HOST: str = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    DB_NAME: str = os.getenv('PERSONAL_DATA_DB_NAME', 'users')

    db: mysql.connector.connection.MySQLConnection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return db


def main() -> None:
    """ Main function """
    db: mysql.connector.connection.MYSQLConnection = get_db()
    cursor: mysql.connector.cursor.MySQLCursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    logger: logging.Logger = get_logger()

    for row in cursor:
        log_record: str = f"name={row[0]}; email={row[1]}; phone={row[2]}; "\
            f"ssn={row[3]}; password={row[4]}; ip={row[5]}; "\
            f"last_login={row[6]}; user_agent={row[7]}"
        logger.info(log_record)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
