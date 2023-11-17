import sqlite3
from sqlite3 import Error
import os

from dotenv import load_dotenv

from logs.my_logging import log


class UserNotFounError(Exception):
    pass


load_dotenv()
DB_PATH = os.environ["DB_PATH"]


class Db:
    def init_tables():
        """
        Preparing the database, creating tables of users,
        tasks and sessions.
        """
        initialization(create_users_table)
        initialization(create_tasks_table)
        initialization(create_sessions_table)
        log.info("Database initialized successfully.")

    def create_user(user_data: dict):
        """
        Accepts user_data: dict as input.
        user: ("name", "email", "login", "password")
        """
        ud = user_data
        user = (ud["name"], ud["email"], ud["login"], ud["password"])
        create_query(create_user_template, user)

    def check_user(user_data: dict):
        """
        Recive user_data = dict
        user = (ud["login"], ud["email"])
        If user found - return user tuple.
        Else return None.
        """
        ud = user_data
        user = (ud["login"], ud["email"])
        result, error = fetch_one(check_user_template, user)
        if result != None:
            log.info("'Check_user' User found.")
            return result
        else:
            log.info("'Check_user' User not found.")
            return

    def get_password(user_data: dict):
        """
        Recive user login. user_data: (ud["login"])
        Return user (password, id) or None.
        """
        user = (user_data["login"],)
        data, error = fetch_one(get_password_template, user)
        if error == None and data != None:
            # return hashed_password, user_id
            return data[0], data[1]
        else:
            return (None, None)

    def create_session(session_data: tuple):
        """
        session_data: (uid, expire, user_id)
        """
        create_query(create_session, session_data)

    def check_session(session_id: str):
        """
        session_id: uid. Check active sessions in DB.
        Return session_data: ('uid', 'expire', 'user_id')
        """
        session_id = (session_id,)
        session_data, error = fetch_one(find_session_template, session_id)
        if error != None:
            return None, error
        else:
            if session_data == None:
                log.info("'check_session' Session did not found.")
                return
            else:
                log.info(f"Found one session: '{session_data}'")
                return session_data, None

    def get_tasks(user_id: int):
        """Recive user_id:int"""

        user_id = (user_id,)
        result = fetch_few(find_tasks_template, user_id)
        return result

    def get_task(task_id: int, user_id):
        data = (task_id, user_id)
        task, error = fetch_one(find_one_task_template, data)
        if error != None:
            return None, error
        if error == None and task != None:
            return task, None

    def new_task(data: tuple):
        """data: ('task', 'user_id')"""

        error = create_query(create_todo_template, data)
        if error != None:
            return error

    def update_task(new_data):
        """data: task, completed, id"""

        create_query(update_todo_template, new_data)

    def delete_task(task_id: str):
        """Delete todo by ID"""
        task_id = (task_id, )
        create_query(delete_todo_template, task_id)

    def update_session(new_expire: str, session_id: str):
        """
        Recive new expire datetime and session_id.
        """
        data = (new_expire, session_id)
        error = create_query(update_sessions_date_template, data)
        if error != None:
            return error


def create_query(template: str, data: tuple):
    """
    Accepts query type and user data as input.
    No fetch.
    """
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH)
        log.info("Connection to SQLite DB successful")
        cursor = connection.cursor()
        cursor.execute(template, data)
        connection.commit()
        cursor.close()
        log.info("Query executed successfully")

    except Error as e:
        log.error(f"The error '{e}' occurred")
        return e
    finally:
        if connection:
            connection.close()
            log.info("Connection to SQLite DB closed")

#


def fetch_one(template, data: tuple):
    """
    Accepts template and user_data: tuple as input.
    Return tuple (result, error).
    """
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH)
        log.info("Connection to SQLite DB successful")
        cursor = connection.cursor()
        cursor.execute(template, data)
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        log.info("Query executed successfully")
        return result, None
    except Error as e:
        log.error(f"The error '{e}' occurred")
        return None, e
    finally:
        if connection:
            connection.close()
            log.info("Connection to SQLite DB closed")


def fetch_few(template, data: tuple):
    """
    Accepts template and user_data: tuple as input.
    Return tuple or error.
    """
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH)
        log.info("Connection to SQLite DB successful")
        cursor = connection.cursor()
        cursor.execute(template, data)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        log.info("Query executed successfully")
        return result
    except Error as e:
        log.error(f"The error '{e}' occurred")
        return None
    finally:
        if connection:
            connection.close()
            log.info("Connection to SQLite DB closed")


def initialization(template):
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH)
        log.info("Connection to SQLite DB successful")
        cursor = connection.cursor()
        cursor.execute(template)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        log.info("Query executed successfully")
        return result
    except Error as e:
        log.error(f"The error '{e}' occurred")
        return None
    finally:
        if connection:
            connection.close()
            log.info("Connection to SQLite DB closed")


# Init table users
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(20) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
login VARCHAR(20) NOT NULL UNIQUE,
password VARCHAR(130) NOT NULL
);
"""


# Init table tasks
create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
task VARCHAR(200) NOT NULL,
completed INTEGER NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


# Init table sessions
create_sessions_table = """
CREATE TABLE IF NOT EXISTS sessions(
uid VARCHAR(50) PRIMARY KEY,
expire DATETIME NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


# Запрос на создание сессии
create_session = """
INSERT INTO
sessions (uid, expire, user_id)
VALUES
(?, ?, ?);
"""


# Запрос на создание пользователя
create_user_template = """
INSERT INTO
users (name, email, login, password)
VALUES
(?, ?, ?, ?);
"""


# Поиск пользователя
check_user_template = """
SELECT * FROM users WHERE login = ? OR email = ?;
"""


# Поиск пользоватяля для входа
get_password_template = """
SELECT password, id FROM users WHERE login = ?;
"""


# Поиск сессии
find_session_template = """
SELECT * FROM sessions WHERE uid = ?;
"""


# Tasks search
find_tasks_template = """
SELECT id, task, completed FROM tasks WHERE user_id = ?;
"""

# Task search
find_one_task_template = """
SELECT * FROM tasks WHERE id = ? AND user_id = ?;
"""

# Todo update
update_todo_template = """
UPDATE tasks
SET task = ?, completed = ?
WHERE id = ?;
"""


# Session date update
update_sessions_date_template = """
UPDATE sessions
SET expire = ?
WHERE uid = ?;
"""


# Create new todo
create_todo_template = """
INSERT INTO
tasks (task, completed, user_id)
VALUES
(?, 0, ?);
"""


# Delete todo
delete_todo_template = """
DELETE FROM
tasks
WHERE id = ?;
"""
