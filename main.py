from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import schema_template as schema
from cookie_handler import Cookie

from sqlite3 import Error
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from json.decoder import JSONDecodeError
from email_validator import validate_email, EmailNotValidError
from my_logging import log
from service import Service, UserNotFounError, IncorrectPasswordError
from request import Request
from db_sqlite import Db


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
        Cookie.check_cookie(cookie)

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
                new_cookie = Cookie.make_cookie(user_id)
                Request.respond(self, 200, "json OK", new_cookie)

            except UserNotFounError:
                print("User not found")
            except IncorrectPasswordError:
                print("Incorrect user password")

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass


class TestServer(BaseHTTPRequestHandler, Handlers):

    Db.init_tables()
    Handlers.do_GET
    Handlers.do_POST

    # execute_query(create_user, ("Dima", "qwersadf123@mail.com",
    #               "asldkfj234", "1234fsasdfasg345"))
    # user = ("asldkfj234", "1234fsasdfasg345")
    # u = Db.login_user(user)


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
