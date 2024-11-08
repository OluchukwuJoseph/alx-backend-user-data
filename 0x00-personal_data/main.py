#!/usr/bin/env python3
"""
Main file
"""
import logging

filter_datum = __import__('filtered_logger').filter_datum
RedactingFormatter = __import__('filtered_logger').RedactingFormatter


fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
log_record = logging.LogRecord("my_logger", logging.INFO, 'person.log', None, message, None, None)
formatter.format(log_record)
