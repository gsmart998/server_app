from http.server import HTTPServer, BaseHTTPRequestHandler
import os

from dotenv import load_dotenv

from database.db_init import QueryError, init_tables
from utils.cookie import MyCookie
from utils.host_validate import is_fqdn
from handlers.request import Request
from handlers.handlers import Get, Post, Put, Delete
from logs.my_logging import log
from services.check_session import check_session


class Handlers(Request, BaseHTTPRequestHandler):
    """HTTP Handlers"""

    def main(self, req):
        my_cookie = MyCookie()
        my_cookie.uid = Request.read(self)
        my_cookie.path = self.path
        path = my_cookie.path
        log.info(f"'{req}{path}' request recived.")

        # check valid path in routes
        if path not in routes[req].keys():
            log.error("'do_GET' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
            return
        route = routes[req][path]

        # check if authorization is required
        if route["auth_check"]:
            result = check_session(my_cookie)
            if result == False:
                Request.respond(self, 401, "Auth error.")
                return

        route["handler"](self, my_cookie)

    def do_GET(self):
        req = "Get"
        Handlers.main(self, req)

    def do_POST(self):
        req = "Post"
        Handlers.main(self, req)

    def do_PUT(self):
        req = "Put"
        Handlers.main(self, req)

    def do_DELETE(self):
        req = "Delete"
        Handlers.main(self, req)


class MyServer(Handlers, BaseHTTPRequestHandler):
    try:
        init_tables()
    except QueryError:
        print("Something gone wrong while create DB tables")


routes = {
    "Get": {
        "/todos": {"handler": Get.todos, "auth_check": True}},
    "Post": {
        "/register": {"handler": Post.register, "auth_check": False},
        "/login": {"handler": Post.login, "auth_check": False},
        "/new": {"handler": Post.new, "auth_check": True},
        "/logout": {"handler": Post.logout, "auth_check": True}},
    "Put": {"/todo": {"handler": Put.todo, "auth_check": True}},
    "Delete": {"/delete": {"handler": Delete.delete, "auth_check": True}}}


if __name__ == "__main__":
    try:
        load_dotenv()
        PORT = int(os.environ["PORT"])
        HOST = os.environ["HOST"]

        # validate env data
        if 0 <= PORT <= 65535 and is_fqdn(HOST):
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
