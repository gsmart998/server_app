from datetime import datetime
import json

from database.db_sqlite import UserNotFounError, Db
from email_validator import validate_email, EmailNotValidError
from logs.my_logging import log
from services.pass_handler import Password


class IncorrectPasswordError(Exception):
    pass


class EmailValidationError(Exception):
    pass


class LoginUserError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class SqlQueryExecError(Exception):
    pass


class FetchTodosError(Exception):
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
            raise EmailValidationError(
                "Error occurred during email validation!")

        # Hash user password
        hashed_password = Password.hash_password(user_data["password"])
        user_data["password"] = hashed_password

        checked_user = Db.check_user(user_data)
        # If requsted user exists - raise error
        if checked_user == None:
            Db.create_user(user_data)
        else:
            log.error(
                "'UserAlreadyExistsError'. User with the requested data already exists")
            raise UserAlreadyExistsError(
                "User with the requested data already exists")

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

    def get_todos(user_id: int) -> str:
        """
        Recive user_id, return user todos as json.
        Or empty no_todos if they don't exist.
        """
        todos = Db.get_tasks(user_id)
        if todos == []:
            log.info("Todos not found.")
            no_todos = "You don't have any todos!"
            return no_todos

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
        data = (todo["task"], user_id)
        error = Db.new_task(data)
        if error != None:
            log.error("SQL create new task error.")
            raise SqlQueryExecError("SQL create new task error.")

    def update_todo(update_todo: dict, user_id: str):
        """update_todo: {'id': int, 'task': 'text', 'completed': 0}."""

        task_id = update_todo["id"]
        new_task = update_todo["task"]
        completed = update_todo["completed"]
        new_data = (new_task, completed, task_id)
        # Try to check todo for exist
        old_todo, error = Db.get_task(task_id, user_id)
        if error != None:
            log.error("SQL get task error.")
            raise SqlQueryExecError("SQL get task error.")
        else:
            if old_todo == None:
                log.error(
                    "Todo does not exists, or user doesn't have access rights.")
                raise FetchTodosError(
                    "Todo does not exists, or user doesn't have access rights.")
            else:
                Db.update_task(new_data)

    def delete_todo(todo: dict, user_id):
        """Recive todo:dict with todo id"""
        task_id = todo["id"]
        task, error = Db.get_task(task_id, user_id)
        if error != None:
            log.error("SQL get task error.")
            raise SqlQueryExecError("SQL get task error.")
        else:
            if task == None:
                log.error(
                    "Todo does not exists, or user doesn't have access rights.")
                raise FetchTodosError(
                    "Todo does not exists, or user doesn't have access rights.")
            else:
                print(f"Todo found: '{task}'")
                Db.delete_task(task_id)
                log.info(f"'delte_todo' Task with id: '{
                         task_id}' has been deleted.")

    def logout_user(session_id: str):
        """Check session_id in DB and marks it with current datetime (expired)."""

        new_expire = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        error = Db.update_session(new_expire, session_id)
        if error != None:
            log.error("SQL update session error.")
            raise SqlQueryExecError("SQL update session error.")
