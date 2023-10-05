from datetime import datetime, timedelta
import uuid
from email_validator import validate_email, EmailNotValidError
from pass_handler import Password
from my_logging import log
from db_sqlite import UserNotFounError, Db


class IncorrectPasswordError(Exception):
    pass


class RegisterUserError(Exception):
    pass


class LoginUserError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class Service:
    """Business layer"""
    def register_user(user_data: dict):
        """
        Recive user_data: dict. Validate email. then checks the
        presence of this user in the database. If there is no
        such user, creates a new one.
        """

        try:
            validate_email(user_data["email"])
        except EmailNotValidError as e:
            log.error(e)
            raise RegisterUserError("Error occurred during email validation")

        # Hash user password
        hashed_password = Password.hash_password(user_data["password"])
        user_data["password"] = hashed_password

        try:
            checked_user = Db.check_user(user_data)
            # If requsted user exists - raise error
            if checked_user:
                log.error(
                    "'UserAlreadyExistsError'. User with the requested data already exists")
                raise UserAlreadyExistsError(
                    "User with the requested data already exists")
        except UserNotFounError:
            try:
                Db.create_user(user_data)
            except:
                log.error("Error occurred")  # Need to fix!

    def login_user(user_data: dict) -> int:
        """
        Recive user_data: dict {"login": "test", "password": "test"}
        Return user_id: int
        """
        # Try to check user login in DB and recive password.
        hashed_password, user_id = Db.get_password(user_data)
        if hashed_password == None:
            log.error("'login_user' Requsted user not found")
            raise UserNotFounError("'login_user' Requsted user not found")
        else:
            if Password.check_password(hashed_password, user_data["password"]) == False:
                log.error("'check_password' Error occurred, incorrect password.")
                raise IncorrectPasswordError(
                    "'check_password' Error occurred, incorrect password.")
            else:
                print("Password correct")
                return user_id

    def make_cookie(user_id: int) -> str:
        """
        Recive user_data: id. Create new session in DB.
        And return cookie with session UUID.
        """
        # Unique session ID
        uid = str(uuid.uuid4())
        # Session lifetime - 30 minutes
        expire = str(datetime.now() + timedelta(minutes=30))
        session_data = (uid, expire, user_id)
        # Add to DB new session
        Db.create_session(session_data)  # Add exceptions handler!!!
        log.info(f"New session '{uid}' created.")
        return uid

    def check_cookie(cookie: str):
        session_data = Db.check_session(cookie)
        if session_data == None:
            print("session did not found")
        else:

            print(f"Found one session: '{session_data}'")
            uid, expire, user_id = session_data
            print(uid, type(expire))
            # expire_datetime = datetime.strptime(expire, '%Y-%m-%d %H:%M:%s')
            # print(expire_datetime)
            # print(type(expire_datetime))
        pass

    def logout_user():
        # принимает session id
        # проверяет session id в базе данных и помечает ее завершенной
        pass

    # def get_todos():
    #     pass

    # def get_todo():
    #     pass

    # def check_session():
    #     pass

    # def create_session():
    #     pass
