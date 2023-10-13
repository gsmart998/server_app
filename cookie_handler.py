from db_sqlite import Db
from my_logging import log


import uuid
from datetime import datetime, timedelta


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

    def check_cookie(self):
        """
        Recive cookie. Check it in DB by uid.
        If it exists and not expired - add user_id to my_cookie.
        """
        session_data = Db.check_session(self.uid)
        if session_data == None:
            print("Session did not found.")
            log.info("Session did not found.")

        else:
            print(f"Found one session: '{session_data}'")
            log.info(f"Found one session: '{session_data}'")

            uid, expire, user_id = session_data
            self.user_id = user_id
            print(self.user_id)

            # Convert string expire to data obj
            expire = datetime.strptime(expire, "%d/%m/%Y, %H:%M:%S")
            self.expire_datetime = expire

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
        expire_str = expire.strftime("%d/%m/%Y, %H:%M:%S")
        session_data = (uid, expire_str, self.user_id)
        # Add to DB new session
        Db.create_session(session_data)  # Add exceptions handler!!!
        log.info(f"New session '{uid}' created.")

        # Add new data to my_cookie
        self.uid = uid
        self.expire_datetime = expire
