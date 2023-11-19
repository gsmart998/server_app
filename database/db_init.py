from database.db_main import query
from logs.my_logging import log


class QueryError(Exception):
    pass


def init_tables():
    """
    Preparing the database, creating tables of users,
    tasks and sessions.
    """
    _, error = query("init", create_users_table)
    _, error = query("init", create_tasks_table)
    _, error = query("init", create_sessions_table)
    if error != None:
        log.error("Database initialization failed.")
        raise QueryError("Sql query error.")

    log.info("Database initialized successfully.")


# Init table users
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY,
name VARCHAR(20) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
login VARCHAR(20) NOT NULL UNIQUE,
password VARCHAR(130) NOT NULL
);
"""

# Init table tasks
create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks(
id SERIAL PRIMARY KEY,
task VARCHAR(200) NOT NULL,
completed BOOLEAN NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

# Init table sessions
create_sessions_table = """
CREATE TABLE IF NOT EXISTS sessions(
uid VARCHAR(50) PRIMARY KEY,
expire TIMESTAMP NOT NULL,
user_id INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
);
"""
