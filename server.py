from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import hashlib
from sqlite3 import Error
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from json.decoder import JSONDecodeError
from email_validator import validate_email, EmailNotValidError


host = "localhost"
port = 8000


# Подключение к БД
path = "app_sqlite.db"


# Создание подключение к БД
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection(path)


# Функция выполнения SQL запроса
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Запрос на создание таблицы users
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(20) NOT NULL,
  email VARCHAR(50) NOT NULL UNIQUE,
  login VARCHAR(20) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL
);
"""
execute_query(connection, create_users_table)


# Запрос на создание таблицы tasks
create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task VARCHAR(100) NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""
execute_query(connection, create_tasks_table)


# Запрос на создание пользователя
create_user = """
INSERT INTO
  users (name, email, login, password)
VALUES
  (?, ?, ?, ?);
"""


# Шаблон json файла формы регистрации
register_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "login": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string"},
    },
    "required": ["name", "login", "password", "email"],
    "additionalProperties": False
}


# Функция валидации email адреса
def check_email(email):
    try:
        # validate email
        validate_email(email)
        print("Email is valid")
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        print(str(e))
        return e


# Функция регистрации пользователя
def register_user(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        return Error


class ServerHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Get request recived!")
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()

        self.wfile.write(
            bytes("<html><body><h1>Hello World!</h1></body></html>", "utf-8"))

    def do_POST(self):
        # Получение длины тела запроса
        content_length = int(self.headers["Content-Length"])

        # Получение тела запроса
        body = self.rfile.read(content_length)
        try:
            body = json.loads(body)  # Конвертируем json в словарь
        except JSONDecodeError:
            print("Ошибка чтения json файла!")

        # ------------------------------------

        # Обработка регистрации
        if self.path == "/register":
            try:
                validate(body, register_schema)
                print("Recived POST request /register")

                # Проверяем email пользователя
                if check_email(body["email"]) != None:
                    print("Email error!")  # Нужна расшифровка!

                # Хешируем пароль пользователя
                user_pw = hashlib.sha256(
                    bytes(body["password"], "UTF-8")).hexdigest()
                user_data = (body["name"], body["email"],
                             body["login"], user_pw)

                if register_user(connection, create_user, user_data) == None:
                    response = 200
                    message = f"User {body['login']} was created!"

                else:
                    response = 400
                    # ??? Как вывести ТЕКСТ ошибки?
                    message = str(Error)

            except ValidationError:
                print("Json is not valid!")
                response = 400
                message = "Json is not valid!"

        # Обработка авторизации
        if self.path == "/login":
            print("Получен запрос /login")

        # Обработка выхода
        if self.path == "/logout":
            print("Получен запрос /logout")

         # ------------------------------------

        # Формирование ответа
        self.send_response(response)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes(message, "UTF-8"))

        """if body == b"add":
            print("Add a new user")
            print(self.path)  # self.path - path in URL "/add"
        else:
            """
        # response = BytesIO()
        # response.write(b"This is POST request. ")
        # response.write(b"Received: ")
        # response.write(body)


server = HTTPServer((host, port), ServerHTTP)

print("Server now running...")
server.serve_forever()
server.shutdown()
