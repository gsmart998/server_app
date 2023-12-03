from http.server import HTTPServer

import settings
from database.db_init import QueryError, init_tables
from utils.env_validate import EnvValidate
from http_.main_handler import Handlers
from http_.router.routes import register_routes
from logs.my_logging import log


def run_server():
    try:
        # init tables in DB
        init_tables()

        # init routes in routes.py
        register_routes()

        PORT = settings.PORT
        HOST = settings.HOST

        # validate env data
        EnvValidate.host_validate(HOST, PORT)

        server = HTTPServer((HOST, PORT), Handlers)
        log.info(f"Server now running on: {HOST}:{PORT}...")
        server.serve_forever()

    except (KeyboardInterrupt, EnvironmentError):
        log.error("Server shutdown...")
        server.shutdown()
    except QueryError:
        print("Something gone wrong while create DB tables")


if __name__ == "__main__":
    run_server()
