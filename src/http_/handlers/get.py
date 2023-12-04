from logs.my_logging import log
from http_.request import Request
from services.todo_service import TodoService
from utils.my_errors import MyErrors as err
from services.session_service import SessionService


class Get:
    def todos(self, my_cookie):
        # check authorization
        if SessionService.check_redis_session(my_cookie.user_id, my_cookie.uid) == False:
            Request.respond(self, 401, "Auth error.")
            return
        try:
            todos = TodoService.get_todos(my_cookie.user_id)
            Request.respond(self, 200, todos)

        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")
