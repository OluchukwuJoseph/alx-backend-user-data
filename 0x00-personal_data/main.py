#!/usr/bin/env python3
"""
Main file
"""
import logging

filter_datum = __import__('filtered_logger').filter_datum
RedactingFormatter = __import__('filtered_logger').RedactingFormatter
get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS
get_db = __import__('filtered_logger').get_db


print(filter_datum.__annotations__)
fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
log_record = logging.LogRecord("my_logger", logging.INFO, 'person.log', None, message, None, None)
formatter.format(log_record)


print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))

new_logger: logging.Logger = get_logger()
new_logger.debug("Hello")


db = get_db()
cursor = db.cursor()
print(type(db))
print(type(cursor))
cursor.execute('SELECT COUNT(*) FROM users;')
for row in cursor:
    print(row[0])

cursor.execute('SELECT email FROM users;')
for row in cursor:
    print(row)
cursor.close()
db.close()
