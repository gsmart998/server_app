from logs.my_logging import log
from database.db_main import query


class DbSessions:

    def get_password(user_data: dict):
        """
        Recive user login. user_data: (ud["login"])
        Return user (password, id) or None.
        """
        user = (user_data["login"],)
        data, error = query("fetch_one", get_password_template, user)
        if error != None:
            return None, error
        # return hashed_password, user_id
        # result = (data[0], data[1])
        return data, None

    def create_session(session_data: tuple):
        """
        session_data: (uid, expire, user_id)
        """
        _, error = query("push", create_session, session_data)
        if error != None:
            return error

    def check_session(session_id: str):
        """
        session_id: uid. Check active sessions in DB.
        Return session_data: ('uid', 'expire', 'user_id')
        """
        session_id = (session_id,)
        session_data, error = query(
            "fetch_one", find_session_template, session_id)
        if error != None:
            return None, error

        if session_data == None:
            log.info("'check_session' Session did not found.")
            return

        log.info(f"Found one session: '{session_data}'")
        return session_data, None

    def update_session(new_expire: str, session_id: str):
        """
        Recive new expire datetime and session_id.
        """
        data = (new_expire, session_id)
        _, error = query("push", update_sessions_date_template, data)
        if error != None:
            return error


# Templates:
#
# Query for create new session
create_session = """
INSERT INTO
sessions (uid, expire, user_id)
VALUES
(%s, %s, %s);
"""

# Query for user search
get_password_template = """
SELECT password, id FROM users WHERE login = %s;
"""

# Поиск сессии
find_session_template = """
SELECT * FROM sessions WHERE uid = %s;
"""

# Session date update
update_sessions_date_template = """
UPDATE sessions
SET expire = %s
WHERE uid = %s;
"""
