from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import schema_template as schema

from sqlite3 import Error
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from json.decoder import JSONDecodeError
from email_validator import validate_email, EmailNotValidError
from my_logging import log
from service import Service, UserNotFounError, IncorrectPasswordError
from request import Request


class Handlers(Request):
    """HTTP Handlers"""

    def do_GET(self):
        """- /todos"""
        path, cookie = Request.read(self)
        if path != "/todos":
            Request.respond(self, 404, "error json")
        else:
            if cookie == None:
                pass
                # print("Cookie is None!")
            else:
                pass
                # print(cookie)
            body = Request.parse(self, path)
            print(body)

            Request.respond(self, 200, "test json")

    def do_POST(self):
        """
        - /register
        - /login
        - /logout
        """
        log.info("POST request recived")
        path, cookie = Request.read(self)
        print(f"Cookie recived: '{cookie}'")
        Service.check_cookie(cookie)

        if path == "/register":
            try:
                user_data = Request.parse(self, path)
                Service.register_user(user_data)

            except Exception:
                print("Registration Error")

        if path == "/login":
            try:
                user_data = Request.parse(self, path)
                user_id = Service.login_user(user_data)
                # new_cookie = Service.make_cookie(user_id)
                # Request.respond(self, 200, "json OK", new_cookie)

            except UserNotFounError:
                print("User not found")
            except IncorrectPasswordError:
                print("Incorrect user password")

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass


class TestServer(BaseHTTPRequestHandler, Handlers):
    # Db.init()
    # execute_query(create_user, ("Dima", "qwersadf123@mail.com",
    #               "asldkfj234", "1234fsasdfasg345"))
    # user = ("asldkfj234", "1234fsasdfasg345")
    # u = Db.login_user(user)
    # print(u)
    # print(type(u))
    # test
    data_time_obj = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    print(type(data_time_obj), data_time_obj)
    new_dat = datetime.strptime(data_time_obj, "%d/%m/%Y, %H:%M:%S")
    print(new_dat < datetime.now())

    Handlers.do_GET
    Handlers.do_POST


HOST = "localhost"
PORT = 8000

try:
    server = HTTPServer((HOST, PORT), TestServer)
    print("Server now running...")
    log.info("Server now running...")
    server.serve_forever()

except KeyboardInterrupt:
    server.shutdown()
    print("\nServer shutdown...")
    log.info("Server shutdown...")


#################################################################

# host = "localhost"
# port = 8001


# # Подключение к БД
# db_path = "sqlite_base.db"


# # Создание подключение к БД
# def create_connection(db_path):
#     connection = None
#     try:
#         connection = sqlite3.connect(db_path)
#         log.info("Connection to SQLite DB successful")
#     except Error as e:
#         log.error(f"The error '{e}' occurred")
#     return connection


# connection = create_connection(db_path)


# # Функция выполнения SQL запроса
# def execute_query(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         connection.commit()
#         log.info("Query executed successfully")
#     except Error as e:
#         log.error(f"The error '{e}' occurred")


# #

# # Формирование ответа на запрос
# def respond_json(self, code: int, message: str, cookie: str = None):
#     if code == 200:
#         text = {"status": "ok"}
#         json_message = json.dumps(text, indent=4)

#     elif code == 400:
#         text = {"status": "failure", "errors": message}
#         json_message = json.dumps(text, indent=4)

#     self.send_response(code)
#     self.send_header("Content-Type", "application/json")
#     set_cookie(self, cookie)
#     self.end_headers()
#     self.wfile.write(json_message.encode())
#     log.info("Reply sent")


# # Функция регистрации пользователя
# def register_user(connection, query, data):
#     cursor = connection.cursor()
#     cursor.execute(query, data)
#     connection.commit()
#     log.info("Register query 'register_user' executed successfully")


# # Функция регистрации сессии
# def register_session(connection, query, data):
#     cursor = connection.cursor()
#     cursor.execute(query, data)
#     connection.commit()
#     log.info("Register query 'register_session' executed successfully")


# # Функция авторизации пользователя
# def login_user(connection, user_data):
#     cursor = connection.cursor()
#     cursor.execute(
#         "SELECT id FROM users WHERE login = ? AND password = ?", user_data)
#     user_id = cursor.fetchone()
#     if user_id != None:
#         log.info("Requested user exist")
#         # Генерируем уникальный id сессии
#         uid = str(uuid.uuid4())
#         # Время жизни сессии 30 минут
#         expire = str(datetime.now() + timedelta(minutes=30))
#         data = (uid, expire, user_id[0])
#         register_session(connection, create_session, data)
#         log.info("Registered new session")
#         return (uid, True)

#     else:
#         log.info("Requested user does not exist")
#         return (Error, False)


# def get_cookie(self):
#     cookie = self.headers.get('Cookie')  # Получаем куки
#     return cookie


# def set_cookie(self, uid: str = None):
#     cookie = http.cookies.SimpleCookie()
#     cookie['cookie'] = uid
#     self.send_header("Set-Cookie", cookie)


# Запрос на создание таблицы users
# create_users_table = """
# CREATE TABLE IF NOT EXISTS users (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   name VARCHAR(20) NOT NULL,
#   email VARCHAR(50) NOT NULL UNIQUE,
#   login VARCHAR(20) NOT NULL UNIQUE,
#   password VARCHAR(100) NOT NULL
# );
# """
# execute_query(connection, create_users_table)


# # Запрос на создание таблицы tasks
# create_tasks_table = """
# CREATE TABLE IF NOT EXISTS tasks(
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   task VARCHAR(100) NOT NULL,
#   user_id INTEGER NOT NULL,
#   FOREIGN KEY (user_id) REFERENCES users (id)
# );
# """
# execute_query(connection, create_tasks_table)


# # Запрос на создание таблицы sessions
# create_sessions_table = """
# CREATE TABLE IF NOT EXISTS sessions(
#   uid VARCHAR(50) PRIMARY KEY,
#   expire DATETIME NOT NULL,
#   user_id INTEGER NOT NULL,
#   FOREIGN KEY (user_id) REFERENCES users (id)
# );
# """
# execute_query(connection, create_sessions_table)


# # Запрос на создание сессии
# create_session = """
# INSERT INTO
#   sessions (uid, expire, user_id)
# VALUES
#   (?, ?, ?);
# """


# # Запрос на создание пользователя
# create_user = """
# INSERT INTO
#   users (name, email, login, password)
# VALUES
#   (?, ?, ?, ?);
# """


# # Шаблон json файла формы регистрации
# register_schema = {
#     "type": "object",
#     "properties": {
#         "name": {"type": "string"},
#         "login": {"type": "string"},
#         "password": {"type": "string"},
#         "email": {"type": "string"},
#     },
#     "required": ["name", "login", "password", "email"],
#     "additionalProperties": False
# }

# # Шаблон json файла формы авторизации
# login_schema = {
#     "type": "object",
#     "properties": {
#         "login": {"type": "string"},
#         "password": {"type": "string"}
#     },
#     "required": ["login", "password"],
#     "additionalProperties": False
# }


# class Server_HTTP(BaseHTTPRequestHandler):
#     def do_GET(self):
#         log.info("GET request recived!")
#         # cookie_string = self.headers.get('Cookie')  # Получаем куки
#         # cookie = get_cookie(self)
#         self.send_response(200)
#         self.send_header("content-type", "text/html")
#         # set_cookie(self)
#         self.end_headers()
#         self.wfile.write(
#             bytes("<html><body><h1>Hello World!</h1></body></html>", "utf-8"))

#     def do_POST(self):
#         log.info("POST request recived")
#         # Обработка регистрации
#         if self.path == "/register":
#             try:
#                 # Получение длины тела запроса
#                 content_length = int(self.headers["Content-Length"])

#                 # Получение тела запроса
#                 body = self.rfile.read(content_length)
#                 body = json.loads(body)  # Конвертируем json в словарь

#                 # Валидация полей JSON файла
#                 validate(body, register_schema)

#                 # Проверяем email пользователя
#                 validate_email(body["email"])

#                 # Хешируем пароль пользователя
#                 user_pw = hashlib.sha256(
#                     bytes(body["password"], "UTF-8")).hexdigest()
#                 user_data = (body["name"], body["email"],
#                              body["login"], user_pw)

#                 # Заносим данные в БД
#                 register_user(connection, create_user, user_data)

#                 # Если нет ошибок отправляем что все ок
#                 respond_json(self, 200, "User created!")
#                 log.info(f"User '{body['login']}' created")

#             # Отрабатываем ошибки
#             # JSON parse error
#             except JSONDecodeError:
#                 respond_json(self, 400, "Ошибка чтения json файла!")
#                 log.error("Ошибка чтения json файла!")

#             # JSON format error
#             except ValidationError as e:
#                 respond_json(self, 400, f"Json is not valid! Error'{e}'")
#                 log.error(f"Json is not valid! Error'{e}'")

#             # Email validation error
#             except EmailNotValidError as e:
#                 respond_json(self, 400, f"Error '{e}' occurred")
#                 log.error(f"Error '{e}' occurred")

#             # SQL error
#             except Error as e:
#                 respond_json(self, 400, f"The error '{e}' occurred")
#                 log.error(f"SQL query ERROR. The error '{e}' occurred")

#         # =====================
#         # Обработка авторизации
#         if self.path == "/login":
#             try:
#                 # Получение длины тела запроса
#                 content_length = int(self.headers["Content-Length"])

#                 # Получение тела запроса
#                 body = self.rfile.read(content_length)
#                 body = json.loads(body)  # Конвертируем json в словарь

#                 # Валидация полей JSON файла
#                 validate(body, login_schema)

#                 # Хешируем пароль пользователя
#                 user_pw = hashlib.sha256(
#                     bytes(body["password"], "UTF-8")).hexdigest()
#                 user_data = (body["login"], user_pw)

#                 login = login_user(connection, user_data)
#                 uid = login[0]
#                 if login[1] == True:
#                     pass

#                 elif login[1] == False:
#                     pass

#                 respond_json(self, 200, "Ok!", uid)

#             # JSON format error
#             except ValidationError as e:
#                 # respond_json(self, 400, f"Json is not valid! Error'{e}'")
#                 log.error(f"Json is not valid! Error'{e}'")

#         # Обработка выхода
#         if self.path == "/logout":
#             pass
#             # print("Получен запрос /logout")
