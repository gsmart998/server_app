import os

from dotenv import load_dotenv

# load data from .env if docker did not provide this information
load_dotenv()

# main service data
PORT = int(os.environ["PORT"])
HOST = os.environ["HOST"]

# PostgreSQL database data
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DATABASE = os.environ["DATABASE"]

# number of attempts to connect to the PostgreSQL database
DB_CONNECT_ATTEMPTS = 10

# redis config
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])

# TTL - time to live for session (in seconds)
TTL = 3600
