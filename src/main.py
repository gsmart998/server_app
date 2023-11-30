from http.server import HTTPServer, BaseHTTPRequestHandler
import os

from database.db_init import QueryError, init_tables
from utils.cookie import MyCookie
from utils.env_validate import EnvValidate
from handlers.request import Request
from handlers.routes import Routes
from logs.my_logging import log
from services.check_session import check_session


class Handlers(Request, BaseHTTPRequestHandler):
    """
    HTTP Handlers
    """

    def main(self, method):
        routes = Routes()
        if method == "init":
            return
        my_cookie = MyCookie()
        my_cookie.uid = Request.read(self)
        my_cookie.path = self.path
        path = my_cookie.path
        log.info(f"'{method}{path}' request recived.")

        # check valid path in routes
        if routes.check_path(method, path) == False:
            log.error("'do_GET' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
            return

        # check if authorization is required
        if routes.auth_check(method, path) == True:
            result = check_session(my_cookie)
            if result == False:
                Request.respond(self, 401, "Auth error.")
                return

        handler = routes.get_handler(method, path)
        handler(self, my_cookie)

    def do_GET(self):
        method = "Get"
        Handlers.main(self, method)

    def do_POST(self):
        method = "Post"
        Handlers.main(self, method)

    def do_PUT(self):
        method = "Put"
        Handlers.main(self, method)

    def do_DELETE(self):
        method = "Delete"
        Handlers.main(self, method)

    try:
        # init tables in DB
        init_tables()
        # init routes in routes.py
        main("init", "init")
    except QueryError:
        print("Something gone wrong while create DB tables")


if __name__ == "__main__":
    try:
        PORT = int(os.environ["PORT"])
        HOST = os.environ["HOST"]

        # validate env data
        EnvValidate.host_validate(HOST, PORT)

        server = HTTPServer((HOST, PORT), Handlers)
        print(f"Server now running on: {HOST}:{PORT}...")
        log.info(f"Server now running on: {HOST}:{PORT}...")
        server.serve_forever()

    except (KeyboardInterrupt, EnvironmentError):
        print("\nServer shutdown...")
        log.error("Server shutdown...")
        server.shutdown()
