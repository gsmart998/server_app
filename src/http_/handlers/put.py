from logs.my_logging import log
from http_.request import Request, ParseErorr
from services.todo_service import TodoService
from utils.my_errors import MyErrors as err
from services.session_service import SessionService


class Put:
    def todo(self, my_cookie):
        # check authorization
        if SessionService.check_redis_session(my_cookie.user_id, my_cookie.uid) == False:
            Request.respond(self, 401, "Auth error.")
            return
        try:
            update_todo = Request.parse(self, update_todo_schema)
            TodoService.update_todo(update_todo, my_cookie.user_id)
            Request.respond(self, 200, "Todo has been updated.")
            log.info("Todo has been updated.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")
        except err.FetchTodosError:
            Request.respond(
                self, 400, "Todo does not exists, or user doesn't have access rights.")


# Template for Request.parse update todo
update_todo_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "task": {"type": "string"},
        "completed": {"type": "boolean"}
    },
    "required": ["id", "task", "completed"],
    "additionalProperties": False
}
