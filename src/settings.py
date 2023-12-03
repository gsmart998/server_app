import os

from dotenv import load_dotenv

# load data from .env if docker did not provide this information
load_dotenv()

# main service data
PORT = int(os.environ["PORT"])
HOST = os.environ["HOST"]

# database data
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DATABASE = os.environ["DATABASE"]
