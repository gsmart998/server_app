from database.db_tasks import DbTasks
from logs.my_logging import log
from utils.my_errors import MyErrors as err


class TodoService:
    def get_todos(user_id: int) -> dict:
        """
        Recive user_id, return user todos as dict.
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
        return todos_list

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
