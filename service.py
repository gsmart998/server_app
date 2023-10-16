from datetime import datetime
import json
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
                log.error("Error occurred")  # Handle exception

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
                log.info("'login_user' Password correct.")
                return user_id

    def get_todos(user_id: int):
        """
        Recive user_id, return user todos as json.
        """
        todos = Db.get_tasks(user_id)
        if todos == None:
            log.info("Todos not found.")
            print("Todos not found.")

        sample = ("id", "text", "completed")
        todos_list = []
        for i in range(len(todos)):
            todo = todos[i]
            res = {sample: todo for sample, todo in zip(sample, todo)}
            if res["completed"] == 0:
                res["completed"] = False
            elif res["completed"] == 1:
                res["completed"] = True
            else:
                res["completed"] = "Wrong status code."
            todos_list.append(res)
        todos_json = json.dumps(todos_list)
        return todos_json

    def create_todo(todo: dict, user_id: str):
        """Recive new todo as dict and user id. Add it to DB.
        todo: {"task": "text", "completed": 0}.
        """
        data = (todo["task"], todo["completed"], user_id)
        Db.new_task(data)

    def update_todo(update_todo: dict, user_id: str):
        """update_todo: {'id': int, 'task': 'text', 'completed': 0}."""

        task_id = update_todo["id"]
        new_task = update_todo["task"]
        completed = update_todo["completed"]
        new_data = (new_task, completed, task_id)
        # Try to check todo for exist
        old_todo = Db.get_task(task_id, user_id)

        if old_todo == None:
            log.error("Todo does not exists, or user doesn't have access rights.")
            # handle error
        else:
            Db.update_task(new_data)

    def delete_todo(todo: dict, user_id):
        """Recive todo:dict with todo id"""
        task_id = todo["id"]
        task = Db.get_task(task_id, user_id)
        if task == None:
            print("Todo with current ID didn't found.")
        else:
            print(f"Todo found: '{task}'")
            Db.delete_task(task_id)
            log.info(f"'delte_todo' Task with id: '{
                     task_id}' has been deleted.")

    def logout_user(session_id: str):
        """Check session_id in DB and marks it with current datetime (expired)."""

        new_expire = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        Db.update_session(new_expire, session_id)
