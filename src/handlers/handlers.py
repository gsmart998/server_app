from utils.cookie import MyCookie
from logs.my_logging import log
from handlers.request import Request, ParseErorr
from services.check_session import check_session
from services.service import Service
from services.my_errors import MyErrors as err


class Get:
    def todos(self, my_cookie):
        try:
            todos = Service.get_todos(my_cookie.user_id)
            Request.respond(self, 200, todos)

        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")


class Post:
    def register(self, my_cookie):
        try:
            user_data = Request.parse(self, my_cookie.path)
            Service.register_user(user_data)
            Request.respond(self, 200, f"User '{
                            user_data['login']}' successfully registered.")
            log.info(f"New user: '{
                user_data['login']}' successfully registered.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except err.EmailValidationError:
            Request.respond(
                self, 400, "Error, email is not valid!")
        except err.UserAlreadyExistsError:
            Request.respond(
                self, 400, "Error, user with the requested data already exists!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")

    def login(self, my_cookie):
        try:
            user_data = Request.parse(self, my_cookie.path)
            my_cookie.user_id = Service.login_user(user_data)
            error = my_cookie.new_uid()
            if error != None:
                Request.respond(
                    self, 503, "Sql query execution error. Try again later.")
                return

            Request.respond(
                self, 200, "User has been authorized.", my_cookie.uid)
            log.info("User has been authorized.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except (err.UserNotFounError, err.IncorrectPasswordError):
            Request.respond(
                self, 400, "Error, incorrect login or password entered!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")

    def new(self, my_cookie):
        try:
            new_todo = Request.parse(self, my_cookie.path)
            Service.create_todo(new_todo, my_cookie.user_id)
            Request.respond(self, 200, "New todo has been created.")
            log.info("New todo has been created.")

        except ParseErorr:
            Request.respond(
                self, 400, "Error occurred while reading json file!")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")

    def logout(self, my_cookie):
        try:
            Service.logout_user(my_cookie.uid)
            Request.respond(self, 200, "User logged out.")
            log.info(
                f"Session '{my_cookie.uid}' ended. User has logged out.")
        except err.SqlQueryExecError:
            Request.respond(
                self, 503, "Sql query execution error. Try again later.")


class Put:
    def todo(self, my_cookie):
        try:
            update_todo = Request.parse(self, my_cookie.path)
            Service.update_todo(update_todo, my_cookie.user_id)
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


class Delete:
    def delete(self, my_cookie):
        try:
            if check_session(my_cookie) == False:
                Request.respond(self, 401, "Auth error.")
                return
            todo = Request.parse(self, my_cookie.path)
            Service.delete_todo(todo, my_cookie.user_id)
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
