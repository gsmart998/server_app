from database.db_main import query
from logs.my_logging import log


class DbTasks:

    def get_tasks(user_id: int):
        """Recive user_id:int"""

        user_id = (user_id,)
        result, error = query("fetch_few", find_tasks_template, user_id)
        if error != None:
            return None, error
        return result, None

    def get_task(task_id: int, user_id):
        data = (task_id, user_id)
        task, error = query("fetch_one", find_one_task_template, data)
        if error != None:
            return None, error
        return task, None

    def new_task(data: tuple):
        """data: ('task', 'user_id')"""

        _, error = query("push", create_todo_template, data)
        if error != None:
            return error

    def update_task(new_data):
        """data: task, completed, id"""

        _, error = query("push", update_todo_template, new_data)
        if error != None:
            return error

    def delete_task(task_id: str):
        """Delete todo by ID"""

        task_id = (task_id, )
        _, error = query("push", delete_todo_template, task_id)
        if error != None:
            return error


# Templates:
#
# Tasks search
find_tasks_template = """
SELECT id, task, completed FROM tasks WHERE user_id = %s;
"""

# Task search
find_one_task_template = """
SELECT * FROM tasks WHERE id = %s AND user_id = %s;
"""

# Todo update
update_todo_template = """
UPDATE tasks
SET task = %s, completed = %s
WHERE id = %s;
"""


# Create new todo
create_todo_template = """
INSERT INTO
tasks (task, completed, user_id)
VALUES
(%s, FALSE, %s);
"""


# Delete todo
delete_todo_template = """
DELETE FROM
tasks
WHERE id = %s;
"""
