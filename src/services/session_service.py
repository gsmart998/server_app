from database.db_sessions import DbSessions
from logs.my_logging import log

from datetime import datetime


class SqlQueryExecError(Exception):
    pass


class SessionService:
    def check_session(cookie) -> bool:
        """
        Check uid for relevance. Add user_id and expire_datetime to cookie.
        Return True if session OK, else - False and error.
        """
        if cookie.uid == None:
            log.error(
                "'check_session' Error, can't check\
                        session without session_uid.")
            return False

        session_data, error = DbSessions.check_session(cookie.uid)
        if error != None:
            raise SqlQueryExecError("'check_session' SQL error.")

        if session_data == None:
            return False

        _, expire, user_id = session_data

        cookie.user_id = user_id
        cookie.expire_datetime = expire

        if expire < datetime.now():
            log.info(f"Cookie with uid: {cookie.uid} is expired.")
            cookie.expired = True
            return False

        else:
            log.info("Cookie is ok.")
            cookie.expired = False
            return True
