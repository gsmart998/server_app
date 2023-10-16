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
            session_data = Db.check_session(self.uid)
            if session_data == None:
                print("Session did not found.")
                log.info("Session did not found.")
                return False
            else:
                log.info(f"Found one session: '{session_data}'")
                _, expire, user_id = session_data
                # Convert string expire to data obj
                expire_datetime = datetime.strptime(
                    expire, "%d/%m/%Y, %H:%M:%S")
                self.user_id = user_id
                self.expire_datetime = expire_datetime

                if expire_datetime < datetime.now():
                    print("cookie is expired")
                    log.info("Cookie is expired")
                    self.expired = True
                    return False

                else:
                    print("cookie is ok")
                    log.info("Cookie is ok")
                    self.expired = False
                    return True
