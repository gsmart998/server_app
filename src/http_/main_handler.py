from http.server import BaseHTTPRequestHandler

from utils.cookie import MyCookie
from http_.request import Request
from http_.router.routes import routes
from logs.my_logging import log


class Handlers(BaseHTTPRequestHandler):
    """
    HTTP Handlers
    """

    def main(self, method):
        path = self.path
        log.info(f"'{method}{path}' request recived.")

        # check valid path in routes
        if routes.check_path(method, path) == False:
            log.error("'do_GET' Wrong '/path'.")
            Request.respond(self, 404, "Wrong '/path'.")
            return

        my_cookie = MyCookie()
        my_cookie.uid, my_cookie.user_id = Request.read(self)
        my_cookie.path = path

        # get specific handler from routes list
        handler = routes.get_handler(method, path)

        # call this handler
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
