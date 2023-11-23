import os
import time

import pg8000.dbapi
from pg8000.dbapi import Error

from logs.my_logging import log


USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DATABASE = os.environ["DATABASE"]


def try_connect_db(attempts: int):
    for i in range(attempts):
        counter = i + 1
        try:
            log.info(f"Try to connect to DB #{counter}")
            connection = pg8000.dbapi.Connection(
                user=USERNAME, password=PASSWORD, host=DB_HOST, port=DB_PORT, database=DATABASE)
            log.info("Connection to DB successful")
            return connection, None
        except Error:
            if counter == attempts:
                log.critical("Connection to DB failed!")
                return None, Error
            log.error("Connection to DB failed, try again...")
            time.sleep(0.5)

            continue


def query(query_type: str, template: str, data: tuple = None):
    """
    Main function to connect to DB
    """
    connection = None
    try:
        connection, error = try_connect_db(15)
        if error != None:
            return None, error

        cursor = connection.cursor()

        if query_type == "init":
            cursor.execute(template)
            connection.commit()
            cursor.close()
            log.info("Query executed successfully")
            return None, None

        cursor.execute(template, data)

        if query_type == "fetch_few":
            result = cursor.fetchall()

        if query_type == "fetch_one":
            result = cursor.fetchone()

        connection.commit()
        cursor.close()
        log.info("Query executed successfully")

        if query_type == "push":
            return None, None

        return result, None

    except Error as e:
        log.error(f"The error '{e}' occurred")
        return None, e
    finally:
        if connection:
            connection.close()
            log.info("Connection to DB closed")
