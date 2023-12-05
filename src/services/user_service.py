from datetime import datetime

from email_validator import validate_email, EmailNotValidError

from database.db_users import DbUsers
from logs.my_logging import log
from utils.pass_validate import Password
from utils.my_errors import MyErrors as err


class UserService:
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
            raise err.EmailValidationError(
                "Error occurred during email validation!")

        # Hash user password
        hashed_password = Password.hash_password(user_data["password"])
        user_data["password"] = hashed_password

        checked_user, error = DbUsers.check_user(user_data)
        if error != None:
            raise err.SqlQueryExecError("'DbUsers.check_user' SQL error.")

        if checked_user == None:
            error = DbUsers.create_user(user_data)
            if error != None:
                raise err.SqlQueryExecError("'DbUsers.create_user' SQL error.")
        else:
            log.error(
                "'UserAlreadyExistsError'. User with the requested data already exists")
            raise err.UserAlreadyExistsError(
                "User with the requested data already exists")

    def login_user(user_data: dict) -> int:
        """
        Recive user_data: dict {"login": "test", "password": "test"}
        Return user_id: int
        """
        # Try to check user login in DB and recive password.
        data, error = DbUsers.get_password(user_data)
        if error != None:
            raise err.SqlQueryExecError("'login_user' SQL get password error.")
        if data == None:
            log.error("'login_user' Requsted user not found")
            raise err.UserNotFounError("'login_user' Requsted user not found")

        hashed_password, user_id = data

        if Password.check_password(hashed_password, user_data["password"]) == False:
            log.error("'check_password' Error occurred, incorrect password.")
            raise err.IncorrectPasswordError(
                "'check_password' Error occurred, incorrect password.")

        log.info("'login_user' Password correct.")
        return user_id
