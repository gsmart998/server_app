
from http.server import HTTPServer, BaseHTTPRequestHandler
from cookie_handler import Cookie
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
        path, cookie = Request.read(self)

        if path != "/todos":
            log.error("Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")

        user_id = Service.auth_check(cookie)
        if user_id == False:
            Request.respond(self, 401, "Auth error.")

        else:
            # Return todo list from db
            todos = Service.get_todos(user_id)

            Request.respond(self, 200, todos)

    def do_POST(self):
        """
        - /register
        - /login
        - /logout
        - /new
        """
        log.info("POST request recived.")
        path, cookie = Request.read(self)
        # print(f"Cookie recived: '{cookie}'")
        # cookie_status = Cookie.check_cookie(cookie)

        if path == "/register":
            log.info("Request '/register'.")
            try:
                user_data = Request.parse(self, path)
                Service.register_user(user_data)
                log.info("User successfully registered.")

            except Exception:
                print("Registration Error")

        if path == "/login":
            log.info("Request '/login'.")
            try:
                user_data = Request.parse(self, path)
                user_id = Service.login_user(user_data)
                new_cookie = Cookie.make_cookie(user_id)
                Request.respond(self, 200, "json OK", new_cookie)
                log.info("User has been authorized.")

            except UserNotFounError:
                print("User not found")
            except IncorrectPasswordError:
                print("Incorrect user password")

        if path == "/logout":
            log.info("Requeset '/logout'.")
            Service.logout_user(cookie)
            Request.respond(self, 200, "User logged out.")
            log.info(f"Session '{cookie}' ended. User has logged out.")

        if path == "/new":
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
        user_id = Service.auth_check(cookie)
        update_todo = Request.parse(self, path)
        Service.update_todo(update_todo, user_id)

        Request.respond(self, 200, "Task updated JSON.")

    def do_DELETE(self):
        pass


class TestServer(BaseHTTPRequestHandler, Handlers):

    Db.init_tables()
    Handlers.do_GET
    Handlers.do_POST


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
