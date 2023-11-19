from datetime import datetime
import json

from database.db_tasks import DbTasks
from database.db_sessions import DbSessions
from database.db_users import DbUsers
from email_validator import validate_email, EmailNotValidError
from logs.my_logging import log
from utils.pass_handler import Password
from services.my_errors import MyErrors as err


class Service:
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
            log.error("Error while execute query.")
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
        data, error = DbSessions.get_password(user_data)
        if error != None:
            raise err.SqlQueryExecError("'login_user' SQL get password error.")
        hashed_password, user_id = data
        if hashed_password == None:
            log.error("'login_user' Requsted user not found")
            raise err.UserNotFounError("'login_user' Requsted user not found")
        else:
            if Password.check_password(hashed_password, user_data["password"]) == False:
                log.error("'check_password' Error occurred, incorrect password.")
                raise err.IncorrectPasswordError(
                    "'check_password' Error occurred, incorrect password.")
            else:
                log.info("'login_user' Password correct.")
                return user_id

    def get_todos(user_id: int) -> str:
        """
        Recive user_id, return user todos as json.
        Or empty no_todos if they don't exist.
        """
        todos, error = DbTasks.get_tasks(user_id)
        if error != None:
            raise err.SqlQueryExecError("'get_todos' SQL get todos error.")

        if todos == ():
            log.info("Todos not found.")
            no_todos = "You don't have any todos!"
            return no_todos

        sample = ("id", "text", "completed")
        todos_list = []
        for i in range(len(todos)):
            todo = todos[i]
            res = {sample: todo for sample, todo in zip(sample, todo)}
            todos_list.append(res)
        todos_json = json.dumps(todos_list)
        return todos_json

    def create_todo(todo: dict, user_id: str):
        """Recive new todo as dict and user id. Add it to DB.
        todo: {"task": "text", "completed": 0}.
        """
        data = (todo["task"], user_id)
        error = DbTasks.new_task(data)
        if error != None:
            raise err.SqlQueryExecError("SQL create new task error.")

    def update_todo(update_todo: dict, user_id: str):
        """update_todo: {'id': int, 'task': 'text', 'completed': 0}."""

        todo_id = update_todo["id"]
        new_todo = update_todo["task"]
        completed = update_todo["completed"]
        new_data = (new_todo, completed, todo_id)

        # Try to check todo for exist
        old_todo, error = DbTasks.get_task(todo_id, user_id)
        if error != None:
            raise err.SqlQueryExecError("SQL get task error.")

        if old_todo == None:
            log.error(
                "Todo does not exists, or user doesn't have access rights.")
            raise err.FetchTodosError(
                "Todo does not exists, or user doesn't have access rights.")

        error = DbTasks.update_task(new_data)
        if error != None:
            raise err.SqlQueryExecError("SQL get task error.")

    def delete_todo(todo: dict, user_id):
        """Recive todo:dict with todo id"""
        task_id = todo["id"]
        task, error = DbTasks.get_task(task_id, user_id)
        if error != None:
            raise err.SqlQueryExecError("SQL get task error.")
        if task == None:
            log.error(
                "Todo does not exists, or user doesn't have access rights.")
            raise err.FetchTodosError(
                "Todo does not exists, or user doesn't have access rights.")

        error = DbTasks.delete_task(task_id)
        if error != None:
            raise err.SqlQueryExecError("SQL get task error.")

        log.info(f"'delte_todo' Task with id: '{task_id}' has been deleted.")

    def logout_user(session_id: str):
        """Check session_id in DB and marks it with current datetime (expired)."""

        new_expire = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        error = DbSessions.update_session(new_expire, session_id)
        if error != None:
            raise err.SqlQueryExecError("SQL update session error.")
