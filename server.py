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


# Формирование ответа на запрос
def respond_json(self, code, message):
    if code == 200:
        text = {"status": "ok"}
        json_message = json.dumps(text, indent=4)

    elif code == 400:
        text = {"status": "failure", "errors": message}
        json_message = json.dumps(text, indent=4)

    self.send_response(code)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json_message.encode())


# Функция регистрации пользователя
def register_user(connection, query, data):
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    print("Query executed successfully")


class Server_HTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Get request recived!")
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()

        self.wfile.write(
            bytes("<html><body><h1>Hello World!</h1></body></html>", "utf-8"))

    def do_POST(self):
        # Обработка регистрации
        if self.path == "/register":
            try:
                # Получение длины тела запроса
                content_length = int(self.headers["Content-Length"])

                # Получение тела запроса
                body = self.rfile.read(content_length)
                body = json.loads(body)  # Конвертируем json в словарь

                # Валидация полей JSON файла
                validate(body, register_schema)
                print("Recived POST request /register")

                # Проверяем email пользователя
                validate_email(body["email"])

                # Хешируем пароль пользователя
                user_pw = hashlib.sha256(
                    bytes(body["password"], "UTF-8")).hexdigest()
                user_data = (body["name"], body["email"],
                             body["login"], user_pw)

                # Заносим данные в БД
                register_user(connection, create_user, user_data)

                # Если нет ошибок отправляем что все ок
                respond_json(self, 200, "User created!")
                print(f"User '{body['login']}' created")

            # Отрабатываем ошибки
            # JSON parse error
            except JSONDecodeError:
                respond_json(self, 400, "Ошибка чтения json файла!")
                print("Ошибка чтения json файла!")

            # JSON format error
            except ValidationError as e:
                respond_json(self, 400, f"Json is not valid! Error'{e}'")
                print(f"Json is not valid! Error'{e}'")

            # Email validation error
            except EmailNotValidError as e:
                respond_json(self, 400, f"Error '{e}' occurred")
                print(f"Error '{e}' occurred")

            # SQL error
            except Error as e:
                respond_json(self, 400, f"The error '{e}' occurred")
                print(f"SQL query ERROR. The error '{e}' occurred")

        # Обработка авторизации
        if self.path == "/login":
            print("Получен запрос /login")

        # Обработка выхода
        if self.path == "/logout":
            print("Получен запрос /logout")


server = HTTPServer((host, port), Server_HTTP)
print("Server now running...")
server.serve_forever()
server.shutdown()
