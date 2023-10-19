
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

from dotenv import load_dotenv

from database.db_sqlite import Db
from handlers.cookie_handler import MyCookie
from handlers.request import Request, ParseErorr
from logs.my_logging import log
from services.service import *


class Handlers(Request):
    """HTTP Handlers"""

    def do_GET(self):
        log.info("GET request '/todos' recived.")
        my_cookie = MyCookie()
        my_cookie.uid, my_cookie.path = Request.read(self)

        if my_cookie.path != "/todos":
            log.error("'do_GET' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
        else:
            if my_cookie.check_session() == False:
                Request.respond(self, 401, "Auth error.")
            else:
                todos = Service.get_todos(my_cookie.user_id)
                Request.respond(self, 200, todos)

    def do_POST(self):
        """/register, /login, /logout, /new """

        log.info("POST request recived.")
        my_cookie = MyCookie()
        my_cookie.uid, my_cookie.path = Request.read(self)

        if my_cookie.path == "/register":
            log.info("Request '/register'.")
            try:
                user_data = Request.parse(self, my_cookie.path)
                Service.register_user(user_data)
                Request.respond(self, 200, f"User '{
                                user_data["login"]}' successfully registered.")
                log.info(f"New user: '{
                         user_data["login"]}' successfully registered.")

            except ParseErorr:
                Request.respond(
                    self, 400, "Error occurred while reading json file!")
            except EmailValidationError:
                Request.respond(
                    self, 400, "Error, email is not valid!")
            except UserAlreadyExistsError:
                Request.respond(
                    self, 400, "Error, user with the requested data already exists!")

        if my_cookie.path == "/login":
            log.info("Request '/login'.")
            try:
                user_data = Request.parse(self, my_cookie.path)
                my_cookie.user_id = Service.login_user(user_data)
                my_cookie.new_uid()
                Request.respond(self, 200, "json OK", my_cookie.uid)
                log.info("User has been authorized.")

            except ParseErorr:
                Request.respond(
                    self, 400, "Error occurred while reading json file!")
            except (UserNotFounError, IncorrectPasswordError):
                Request.respond(
                    self, 400, "Error, incorrect login or password entered!")

        if my_cookie.path == "/logout":
            log.info("Requeset '/logout'.")
            if my_cookie.check_session() == False:
                Request.respond(self, 401, "Auth error.")
            else:
                try:
                    Service.logout_user(my_cookie.uid)
                    Request.respond(self, 200, "User logged out.")
                    log.info(
                        f"Session '{my_cookie.uid}' ended. User has logged out.")
                except SqlQueryExecError:
                    Request.respond(
                        self, 503, "Sql query execution error. Try again later.")
        if my_cookie.path == "/new":
            log.info("Request '/new'.")

            if my_cookie.check_session() == False:
                Request.respond(self, 401, "Auth error.")
            else:
                try:
                    new_todo = Request.parse(self, my_cookie.path)
                    Service.create_todo(new_todo, my_cookie.user_id)
                    Request.respond(self, 200, "Task created JSON.")
                    log.info("New todo has been created.")
                except ParseErorr:
                    Request.respond(
                        self, 400, "Error occurred while reading json file!")
                except SqlQueryExecError:
                    Request.respond(
                        self, 503, "Sql query execution error. Try again later.")

    def do_PUT(self):
        log.info("PUT request recived.")
        my_cookie = MyCookie()
        my_cookie.uid, my_cookie.path = Request.read(self)
        if my_cookie.path != "/todo":
            log.error("Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
        else:
            if my_cookie.check_session() == False:
                Request.respond(self, 401, "Auth error.")
            else:
                try:
                    update_todo = Request.parse(self, my_cookie.path)
                    Service.update_todo(update_todo, my_cookie.user_id)
                    Request.respond(self, 200, "Task updated JSON.")
                except ParseErorr:
                    Request.respond(
                        self, 400, "Error occurred while reading json file!")
                except SqlQueryExecError:
                    Request.respond(
                        self, 503, "Sql query execution error. Try again later.")
                except FetchTodosError:
                    Request.respond(
                        self, 400, "Todo does not exists, or user doesn't have access rights.")

    def do_DELETE(self):
        log.info("DELETE request recived.")
        my_cookie = MyCookie()
        my_cookie.uid, my_cookie.path = Request.read(self)
        if my_cookie.path != "/delete":
            log.error("'do_DELETE' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
        else:
            if my_cookie.check_session() == False:
                Request.respond(self, 401, "Auth error.")
            else:
                try:
                    todo = Request.parse(self, my_cookie.path)
                    Service.delete_todo(todo, my_cookie.user_id)
                    Request.respond(self, 200, "Task has been deleted.")
                except ParseErorr:
                    Request.respond(
                        self, 400, "Error occurred while reading json file!")
                except SqlQueryExecError:
                    Request.respond(
                        self, 503, "Sql query execution error. Try again later.")
                except FetchTodosError:
                    Request.respond(
                        self, 400, "Todo does not exists, or user doesn't have access rights.")


class MyServer(Handlers, BaseHTTPRequestHandler):
    Db.init_tables()


if __name__ == "__main__":
    try:
        load_dotenv()
        PORT = int(os.environ["PORT"])
        HOST = os.environ["HOST"]
        server = HTTPServer((HOST, PORT), MyServer)
        print(f"Server now running on port: {PORT} ...")
        log.info("Server now running...")
        server.serve_forever()

    except KeyboardInterrupt:
        server.shutdown()
        print("\nServer shutdown...")
        log.info("Server shutdown...")
