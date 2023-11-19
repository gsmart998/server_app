import uuid

from database.db_sessions import DbSessions
from datetime import datetime, timedelta
from logs.my_logging import log


class SqlQueryExecError(Exception):
    pass


class MyCookie:
    def __init__(self):
        self.uid = None
        self.user_id = None
        self.path = "/"
        self.expire_datetime = None  # store datetime object
        self.expired = None

    def _print(self):
        print("uid:", self.uid)
        print("user_id", self.user_id)
        print("path", self.path)
        print("expire_time", self.expire_datetime)
        print("expired", self.expired)

    def new_uid(self):
        """
        Generate new session UUID. Create new session in DB.
        And add new data to my_cookie.
        """
        # Unique session ID
        uid = str(uuid.uuid4())
        # Session lifetime - 30 minutes
        expire = datetime.now() + timedelta(minutes=30)
        # Convert to string with custom format
        expire_str = expire.strftime("%Y-%m-%d, %H:%M:%S")
        print(expire_str)
        session_data = (uid, expire_str, self.user_id)
        # Add to DB new session
        error = DbSessions.create_session(session_data)
        if error != None:
            return error

        log.info(f"New session '{uid}' created.")

        # Add new data to my_cookie
        self.uid = uid
        self.expire_datetime = expire
