
import redis
import uuid

from logs.my_logging import log


class SessionService:

    def new_session(user_id: int) -> str:
        """
        Takes user_id: int, generate new session UID.
        Create new session in DB. Return session uid: str.
        """
        # Unique session ID
        uid = str(uuid.uuid4())
        # Add to redis DB new session
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.set(user_id, uid)
        log.info(f"New session '{uid}' created in redis.")
        return uid

    def check_redis_session(user_id: int, uid: str) -> bool:
        """
        Func for check active session in redis DB, search session by
        user_id, then compare session uid from DB and from cookie.
        """
        if uid == None:
            log.error(
                "'check_redis_session' Error, can't check session without any data.")
            return False

        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        res = r.get(user_id)
        if res != uid:
            log.info("Session not found!")
            return False
        log.info("Session found, auth - ok")
        return True

    def end_session(user_id: int):
        """Delete session in redis db with user_id key"""
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.delete(user_id)
