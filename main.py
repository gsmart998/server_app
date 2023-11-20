from http.server import HTTPServer, BaseHTTPRequestHandler
import os

from dotenv import load_dotenv

from database.db_init import QueryError, init_tables
from utils.cookie import MyCookie
from utils.host_validate import is_fqdn
from handlers.request import Request, ParseErorr
from logs.my_logging import log
from services.check_session import check_session
from services.service import Service
from services.my_errors import MyErrors as err


class Handlers(Request):
    """HTTP Handlers"""

    def do_GET(self):
        log.info("GET request '/todos' recived.")
        my_cookie = MyCookie()
        my_cookie.uid, my_cookie.path = Request.read(self)

        if my_cookie.path != "/todos":
            log.error("'do_GET' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
            return
        
        try:
            result = check_session(my_cookie)
            if result == False:
                Request.respond(self, 401, "Auth error.")
                return
            
            todos = Service.get_todos(my_cookie.user_id)
            Request.respond(self, 200, todos)
            
        except err.SqlQueryExecError:
            Request.respond(self, 503, "Sql query execution error. Try again later.")

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
            except err.EmailValidationError:
                Request.respond(
                    self, 400, "Error, email is not valid!")
            except err.UserAlreadyExistsError:
                Request.respond(
                    self, 400, "Error, user with the requested data already exists!")
            except err.SqlQueryExecError:
                Request.respond(
                        self, 503, "Sql query execution error. Try again later.")

        if my_cookie.path == "/login":
            log.info("Request '/login'.")
            try:
                user_data = Request.parse(self, my_cookie.path)
                my_cookie.user_id = Service.login_user(user_data)
                error = my_cookie.new_uid()
                if error != None:
                    Request.respond(
                        self, 503, "Sql query execution error. Try again later.")
                    return
                
                Request.respond(self, 200, "User has been authorized.", my_cookie.uid)
                log.info("User has been authorized.")

            except ParseErorr:
                Request.respond(
                    self, 400, "Error occurred while reading json file!")
            except (err.UserNotFounError, err.IncorrectPasswordError):
                Request.respond(
                    self, 400, "Error, incorrect login or password entered!")
            except err.SqlQueryExecError:
                Request.respond(
                        self, 503, "Sql query execution error. Try again later.")

        if my_cookie.path == "/logout":
            log.info("Requeset '/logout'.")
            try:
                if check_session(my_cookie) == False:
                    Request.respond(self, 401, "Auth error.")
                    return
                Service.logout_user(my_cookie.uid)
                Request.respond(self, 200, "User logged out.")
                log.info(
                    f"Session '{my_cookie.uid}' ended. User has logged out.")
            except err.SqlQueryExecError:
                Request.respond(
                    self, 503, "Sql query execution error. Try again later.")
                
        if my_cookie.path == "/new":
            log.info("Request '/new'.")
            try:
                if check_session(my_cookie) == False:
                    Request.respond(self, 401, "Auth error.")
                    return
                new_todo = Request.parse(self, my_cookie.path)
                Service.create_todo(new_todo, my_cookie.user_id)
                Request.respond(self, 200, "New todo has been created.")
                log.info("New todo has been created.")
            except ParseErorr:
                Request.respond(
                    self, 400, "Error occurred while reading json file!")
            except err.SqlQueryExecError:
                Request.respond(
                    self, 503, "Sql query execution error. Try again later.")

    def do_PUT(self):
        log.info("PUT request recived.")
        my_cookie = MyCookie()
        my_cookie.uid, my_cookie.path = Request.read(self)
        if my_cookie.path != "/todo":
            log.error("Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
            return
        try:
            if check_session(my_cookie) == False:
                Request.respond(self, 401, "Auth error.")
                return
            update_todo = Request.parse(self, my_cookie.path)
            Service.update_todo(update_todo, my_cookie.user_id)
            Request.respond(self, 200, "Todo has been updated.")
            log.info("Todo has been updated.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")
        except err.FetchTodosError:
            Request.respond(
                self, 400, "Todo does not exists, or user doesn't have access rights.")

    def do_DELETE(self):
        log.info("DELETE request recived.")
        my_cookie = MyCookie()
        my_cookie.uid, my_cookie.path = Request.read(self)
        if my_cookie.path != "/delete":
            log.error("'do_DELETE' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
            return
        try:
            if check_session(my_cookie) == False:
                Request.respond(self, 401, "Auth error.")
                return
            todo = Request.parse(self, my_cookie.path)
            Service.delete_todo(todo, my_cookie.user_id)
            Request.respond(self, 200, "Task has been deleted.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")
        except err.FetchTodosError:
            Request.respond(
                self, 400, "Todo does not exists, or user doesn't have access rights.")


class MyServer(Handlers, BaseHTTPRequestHandler):
    try:
        init_tables()
    except QueryError:
        print("Something gone wrong while create DB tables")




if __name__ == "__main__":
    try:
        load_dotenv()
        PORT = int(os.environ["PORT"])
        HOST = os.environ["HOST"]

        # validate env data
        if  0 <= PORT <= 65535 and is_fqdn(HOST):
            log.info("Use HOST and PORT data from .ENV file.")

        else:
            # if ENV data incorrect - use default values
            log.error(".ENV data is incorrect, use default HOST and PORT.")
            PORT = 8000
            HOST = "127.0.0.1"
        
        server = HTTPServer((HOST, PORT), MyServer)
        print(f"Server now running on: {HOST}:{PORT}...")
        log.info(f"Server now running on: {HOST}:{PORT}...")
        server.serve_forever()

    except KeyboardInterrupt:
        server.shutdown()
        print("\nServer shutdown...")
        log.info("Server shutdown...")

