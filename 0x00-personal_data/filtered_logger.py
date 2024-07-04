#!/usr/bin/env python3
""" filtered_logger.py """
import re
import logging
from typing import List
from os import getenv
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    FIELDS = []

    def __init__(self, fields: List[str]):
        """ RedactingFormatter constructor """
        self.FIELDS = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ filters values in incoming log records using filter_datum """
        return filter_datum(self.FIELDS, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    items = message.split(separator)
    for i, item in enumerate(items):
        for field in fields:
            items[i] = re.sub(fr'{field}=.*', f'{field}={redaction}', items[i])
    return separator.join(items)


PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']


def get_logger() -> logging.Logger:
    """ returns a logger with specific properties """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter)
    logger.addHandler(sh)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database """
    username = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = getenv('PERSONAL_DATA_DB_NAME')
    cnx = mysql.connector.Connect(
        host=host,
        port=3306,
        user=username,
        password=password,
        database=database
    )
    return cnx


def main() -> None:
    """ obtains a database connection using get_db
    and retrieves all rows in the users table
    and displays each row under a filtered format """
    logger = get_logger()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    fields = ['name', 'email', 'phone', 'ssn', 'password',
              'ip', 'last_login', 'user_agent']

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        row = list(row)
        row[6] = row[6].strftime("%Y-%m-%d %H:%M:%S")
        row = [f'{fields[i]}={row[i]}' for i in range(len(fields))]
        log_record = logging.LogRecord("user_data", logging.INFO, None,
                                       None, '; '.join(row), None, None)
        print(formatter.format(log_record))
    cursor.close()
    db.close()


if __name__ == '__main__':
    """ runs when the module is executed """
    main()
