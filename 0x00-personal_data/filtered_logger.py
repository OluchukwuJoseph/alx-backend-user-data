#!/usr/bin/env python3
"""
This script contains functions and classes
for logging user data Redactingly
"""
from typing import List, Tuple, Dict
import re
import logging
import os
import mysql.connector


PII_FIELDS: Tuple = ('name', 'ssn', 'password', 'email', 'phone')


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """ Returns the log message obfuscated """
    new_message = re.sub(rf'({"|".join(fields)})=[^{seperator}]+',
                         rf'\1={redaction}', message)
    return new_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION: str = "***"
    FORMAT: str = "[HOLBERTON] %(name)s %(levelname)s "\
        "%(asctime)-15s: %(message)s"
    SEPERATOR: str = ';'

    def __init__(self, fields: List[str]):
        """ Initializies instance """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Return formatted log record """
        message: str = filter_datum(self.fields, self.REDACTION,
                                    record.msg, self.SEPERATOR)
        record.msg = message
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """ Returns a Logger object """
    new_logger: logging.Logger = logging.getLogger('user_data')
    new_logger.setLevel(logging.INFO)
    new_logger.propagate = False
    console_handler: logging.Handler = logging.StreamHandler()
    console_handler.setFormatter(RedactingFormatter(fields=list(PII_FIELDS)))
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
    DB_NAME: str = os.getenv('PERSONAL_DATA_DB_NAME')

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

    if cursor.description is not None:
        columns = []
        for column_desc in cursor.description:
            columns.append(column_desc[0])

    for row in cursor.fetchall():
        message = '; '.join(f"{col}={value}" for col, value
                            in zip(columns, row))
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
