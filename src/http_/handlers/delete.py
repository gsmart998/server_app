from logs.my_logging import log
from http_.request import Request, ParseErorr
from services.session_service import SessionService
from services.todo_service import TodoService
from utils.my_errors import MyErrors as err


class Delete:
    def delete(self, uid, user_id):
        # check authorization
        if SessionService.check_redis_session(user_id, uid) == False:
            Request.respond(self, 401, "Auth error.")
            return
        try:
            todo = Request.parse(self, delete_todo_schema)
            TodoService.delete_todo(todo, user_id)
            Request.respond(self, 200, "Task has been deleted.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")
        except err.FetchTodosError:
            Request.respond(
                self, 400, "Todo does not exists, or user doesn't have access rights.")
        except err.RedisConnectionError:
            Request.respond(
                self, 503, "Internal error. Try again later.")


# Template for Request.parse
delete_todo_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"}
    },
    "required": ["id"],
    "additionalProperties": False
}
