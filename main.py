
from http.server import HTTPServer, BaseHTTPRequestHandler
import uuid
from cookie_handler import MyCookie
from sqlite3 import Error
from my_logging import log
from service import Service, UserNotFounError, IncorrectPasswordError
from request import Request
from db_sqlite import Db


class Handlers(Request):
    """HTTP Handlers"""

    def do_GET(self):
        """/todos"""

        log.info("GET request '/todos' recived.")
        my_cookie = MyCookie()
        Request.read(self, my_cookie)

        if my_cookie.path != "/todos":
            log.error("'do_GET' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")

        else:
            if Service.auth_check(my_cookie) == False:
                Request.respond(self, 401, "Auth error.")

            else:
                todos = Service.get_todos(my_cookie.user_id)
                Request.respond(self, 200, todos)

        my_cookie._print()  # test

    def do_POST(self):
        """/register, /login, /logout, /new """

        log.info("POST request recived.")
        my_cookie = MyCookie()
        Request.read(self, my_cookie)

        if my_cookie.path == "/register":
            log.info("Request '/register'.")
            try:
                user_data = Request.parse(self, my_cookie.path)
                Service.register_user(user_data)  # Fix register_user func
                Request.respond(self, 200, "User successfully registered.")
                log.info("User successfully registered.")

            except Exception:
                print("Registration Error")

        if my_cookie.path == "/login":
            log.info("Request '/login'.")
            try:
                user_data = Request.parse(self, my_cookie.path)
                Service.login_user(user_data, my_cookie)
                my_cookie.new_uid()
                Request.respond(self, 200, "json OK", my_cookie.uid)
                log.info("User has been authorized.")

                my_cookie._print()  # test

            except UserNotFounError:
                print("User not found")
            except IncorrectPasswordError:
                print("Incorrect user password")

        if my_cookie.path == "/logout":
            log.info("Requeset '/logout'.")
            Service.logout_user(cookie)
            Request.respond(self, 200, "User logged out.")
            log.info(f"Session '{cookie}' ended. User has logged out.")

        if my_cookie.path == "/new":
            log.info("Request '/new'.")
            user_id = Service.auth_check(cookie)
            if user_id == False:
                Request.respond(self, 401, "Auth error.")
            else:
                new_todo = Request.parse(self, path)
                Service.create_todo(new_todo, user_id)
                Request.respond(self, 200, "Task created JSON.")
                log.info("New todo has been created.")

    def do_PUT(self):
        log.info("PUT request recived.")
        path, cookie = Request.read(self)
        if path != "/todo":
            log.error("Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
        else:
            user_id = Service.auth_check(cookie)
            if user_id == False:
                Request.respond(self, 401, "Auth error.")
            else:
                update_todo = Request.parse(self, path)
                Service.update_todo(update_todo, user_id)

                Request.respond(self, 200, "Task updated JSON.")

    def do_DELETE(self):
        log.info("DELETE request recived.")
        path, cookie = Request.read(self)
        if path != "/delete":
            log.error("'do_DELETE' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
        else:
            user_id = Service.auth_check(cookie)
            if user_id == False:
                Request.respond(self, 401, "Auth error.")
            else:
                todo = Request.parse(self, path)
                Service.delete_todo(todo, user_id)
                Request.respond(self, 200, "Task has been deleted.")


class TestServer(Handlers, BaseHTTPRequestHandler):

    Db.init_tables


HOST = "localhost"
PORT = 8000

if __name__ == "__main__":
    try:
        server = HTTPServer((HOST, PORT), TestServer)
        print("Server now running...")
        log.info("Server now running...")
        server.serve_forever()

    except KeyboardInterrupt:
        server.shutdown()
        print("\nServer shutdown...")
        log.info("Server shutdown...")
