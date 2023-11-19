import os

import pg8000.dbapi
from pg8000.dbapi import Error
from dotenv import load_dotenv

from logs.my_logging import log


load_dotenv()
USERNAME = (os.environ["USERNAME"])
PASSWORD = (os.environ["PASSWORD"])
DB_HOST = (os.environ["DB_HOST"])
DB_PORT = (os.environ["DB_PORT"])
DATABASE = (os.environ["DATABASE"])


def query(query_type: str, template: str, data: tuple = None):
    """
    Recives query_type: ("push", "fetch_one", "fetch_few", "init")
    """
    connection = None
    try:
        connection = pg8000.dbapi.Connection(
            user=USERNAME, password=PASSWORD, host=DB_HOST, port=DB_PORT, database=DATABASE)
        log.info("Connection to SQLite DB successful")
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
