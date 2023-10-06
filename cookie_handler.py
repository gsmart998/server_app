from db_sqlite import Db
from my_logging import log


import uuid
from datetime import datetime, timedelta


class Cookie:
    def make_cookie(user_id: int) -> str:
        """
        Recive user_data: id. Create new session in DB.
        And return cookie with session UUID.
        """
        # Unique session ID
        uid = str(uuid.uuid4())
        # Session lifetime - 30 minutes
        expire = datetime.now() + timedelta(minutes=30)
        # Convert to string with custom format
        expire = expire.strftime("%d/%m/%Y, %H:%M:%S")
        session_data = (uid, expire, user_id)
        # Add to DB new session
        Db.create_session(session_data)  # Add exceptions handler!!!
        log.info(f"New session '{uid}' created.")
        return uid

    def check_cookie(cookie: str) -> bool:
        """
        Recive cookie (seesion uid). Check it in DB.
        If it exists and not expired - return True.
        Else - return False
        """
        session_data = Db.check_session(cookie)
        if session_data == None:
            print("Session did not found.")
            log.info("Session did not found.")
            return False
        else:
            print(f"Found one session: '{session_data}'")
            log.info(f"Found one session: '{session_data}'")
            uid, expire, user_id = session_data

            # Convert string expire to data obj
            expire = datetime.strptime(expire, "%d/%m/%Y, %H:%M:%S")
            if expire < datetime.now():
                print("cookie is expired")
                log.info("Cookie is expired")
                return False
            else:
                print("cookie is ok")
                log.info("Cookie is ok")
                return True
