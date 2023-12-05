import redis
import uuid

import settings
from utils.my_errors import MyErrors as err
from logs.my_logging import log


REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
TTL = settings.TTL


class SessionService:

    def new_session(user_id: int) -> str:
        """
        Takes user_id: int, generate new session UID.
        Create new session in DB. Return session uid: str.
        """
        # Unique session ID
        uid = str(uuid.uuid4())
        # Add to redis DB new session with expire time TTL
        try:
            conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                               decode_responses=True)
            conn.set(user_id, uid, ex=TTL)

        except redis.exceptions.ConnectionError as e:
            log.error(f"Error occurred while connect to redis DB:'{e}'")
            raise err.RedisConnectionError("Can't connect to redis")

        log.info(f"New session '{uid}' created in DB.")
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

        try:
            conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                               decode_responses=True)
            res = conn.get(user_id)

        except redis.exceptions.ConnectionError as e:
            log.error(f"Error occurred while connect to redis DB:'{e}'")
            raise err.RedisConnectionError("Can't connect to redis")

        if res != uid:
            log.info("Session not found!")
            return False

        log.info("Session found, auth - ok")
        return True

    def end_session(user_id: int):
        """Delete session in redis db with user_id key"""
        try:
            conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                               decode_responses=True)
            conn.delete(user_id)

        except redis.exceptions.ConnectionError as e:
            log.error(f"Error occurred while connect to redis DB:'{e}'")
            raise err.RedisConnectionError("Can't connect to redis")
