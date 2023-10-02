import sqlite3
from sqlite3 import Error
from my_logging import log


class UserNotFounError(Exception):
    pass


class Db:
    def create_user(user_data: dict):
        """
        Accepts user_data: dict as input.
        user: ("name", "email", "login", "password")
        """
        ud = user_data
        user = (ud["name"], ud["email"], ud["login"], ud["password"])
        create_query(create_user_template, user)

    def check_user(user_data: dict) -> tuple:
        """
        Recive user_data = dict
        user = (ud["login"], ud["email"])
        If user found - return user tuple.
        Else raise UserNotFoundError
        Or SQL connection Erorr
        """
        ud = user_data
        user = (ud["login"], ud["email"])
        result = fetch_one(check_user_template, user)
        if result != None:
            return result
        else:
            log.error("'Check_user' User not found")
            raise UserNotFounError("'Check_user' User not found")

    def get_password(user_data: dict):
        """
        Recive user login. user_data: (ud["login"])
        Return user password.
        """
        user = (user_data["login"],)
        password = fetch_one(get_password_template, user)
        if password != None:
            return (password[0])
        else:
            raise UserNotFounError("'get_password' User not found")


def create_query(template: str, data: tuple):
    """
    Accepts query type and user data as input.
    No fetch.
    """
    connection = None
    try:
        connection = sqlite3.connect("sqlite_base.db")
        log.info("Connection to SQLite DB successful")
        cursor = connection.cursor()
        cursor.execute(template, data)
        connection.commit()
        cursor.close()
        log.info("Query executed successfully")

    except Error as e:
        log.error(f"The error '{e}' occurred")
        return None, e
    finally:
        if connection:
            connection.close()
            log.info("Connection to SQLite DB closed")


def fetch_one(template, data: tuple) -> tuple:
    """
    Accepts template and user_data: tuple as input.
    Return tuple or error.
    """
    connection = None
    try:
        connection = sqlite3.connect("sqlite_base.db")
        log.info("Connection to SQLite DB successful")
        cursor = connection.cursor()
        cursor.execute(template, data)
        result = cursor.fetchone()
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


def fetch_few(template, data: tuple):
    """
    Accepts template and user_data: tuple as input.
    Return tuple or error.
    """
    connection = None
    try:
        connection = sqlite3.connect("sqlite_base.db")
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


# def login_user(user_data: dict):
#     """user = (ud["login"], ud["password"])"""
#     connection = None
#     ud = user_data
#     user = (ud["login"], ud["password"])
#     try:
#         connection = sqlite3.connect("sqlite_base.db")
#         log.info("Connection to SQLite DB successful")
#         cursor = connection.cursor()
#         cursor.execute(login_user_template, user)
#         result = cursor.fetchone()
#         connection.commit()
#         cursor.close()
#         if result == None:
#             log.error("User not found. Check login and password")
#             raise UserNotFounError("User not found. Check login and password")
#         log.info("Query executed successfully")
#         return result
#     except Error as e:
#         log.error(f"The error '{e}' occurred")

#     finally:
#         if connection:
#             connection.close()
#             log.info("Connection to SQLite DB closed")


# class Db:

    # def init():
    #     execute_query("create_users_table")
    #     execute_query("create_tasks_table")
    #     execute_query("create_sessions_table")

    # def create_user(user_data: tuple):  # create_user
    #     """
    #     Recives the user's data: name, email, login,
    #     password as tuple. Return error.
    #     """
    #     _, error = execute_query("create_user", user_data)
    #     return error

    # def create_session(data):
    #     execute_query("create_session", data)

    # def login_user(data) -> tuple | None:
    #     """
    #     Recive the user's login and password as input.
    #     Returns a tuple with the user if it matches either None.
    #     """
    #     user, error = execute_query("login_user", data)
    #     if user == []:
    #         print("User not found")
    #         return
    #     else:
    #         return user[0]
# Запрос на создание таблицы users
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(20) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
login VARCHAR(20) NOT NULL UNIQUE,
password VARCHAR(130) NOT NULL
);
"""


# Запрос на создание таблицы tasks
create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
task VARCHAR(100) NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


# Запрос на создание таблицы sessions
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
SELECT * FROM users WHERE login = ? AND email = ?;
"""

# Поиск пользоватяля для входа
get_password_template = """
SELECT password FROM users WHERE login = ?;
"""

query_dict = {
    "create_users_table": create_users_table,
    "create_tasks_table": create_tasks_table,
    "create_sessions_table": create_sessions_table,
    "create_session": create_session,
    "create_user": create_user_template,
    "check_user": check_user_template,
    "get_password": get_password_template
}
