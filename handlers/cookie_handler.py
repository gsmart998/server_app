import uuid

from database.db_sqlite import Db
from datetime import datetime, timedelta
from logs.my_logging import log


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
        expire_str = expire.strftime("%d/%m/%Y, %H:%M:%S")
        session_data = (uid, expire_str, self.user_id)
        # Add to DB new session
        Db.create_session(session_data)  # Add exceptions handler!!!
        log.info(f"New session '{uid}' created.")

        # Add new data to my_cookie
        self.uid = uid
        self.expire_datetime = expire

    def check_session(self) -> bool:
        """
        Check uid for relevance. Add user_id and expire_datetime to cookie.
        Return True if session OK, else - False.
        """
        if self.uid == None:
            print("Error, can't check session without session_uid.")
            log.error(
                "'MyCookie.check_cookie' Error, can't check\
                    session without session_uid.")
            return False
        else:
            session_data, error = Db.check_session(self.uid)
            if error != None:
                log.error(error)
                return False
            else:
                if session_data == None:
                    return False
                else:
                    _, expire, user_id = session_data
                    # Convert string expire to data obj
                    expire_datetime = datetime.strptime(
                        expire, "%d/%m/%Y, %H:%M:%S")
                    self.user_id = user_id
                    self.expire_datetime = expire_datetime

                    if expire_datetime < datetime.now():
                        log.info(f"Cookie with uid: {self.uid} is expired.")
                        self.expired = True
                        return False

                    else:
                        log.info("Cookie is ok.")
                        self.expired = False
                        return True
