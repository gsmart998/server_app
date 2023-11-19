import os

import pg8000.dbapi
from dotenv import load_dotenv

load_dotenv()
USERNAME = (os.environ["USERNAME"])
PASSWORD = (os.environ["PASSWORD"])
DB_HOST = (os.environ["DB_HOST"])
DB_PORT = (os.environ["DB_PORT"])
DATABASE = (os.environ["DATABASE"])


connection = pg8000.dbapi.Connection(
    user=USERNAME, password=PASSWORD, host=DB_HOST, port=DB_PORT, database=DATABASE)

cursor = connection.cursor()
cursor.execute("SELECT * FROM users WHERE id = %s AND name = %s", (1, "Admin"))
results = cursor.fetchone()
print(results)
# for row in results:
#     print(row)
connection.commit()
connection.close()
