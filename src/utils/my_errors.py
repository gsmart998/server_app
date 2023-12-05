class MyErrors:
    class UserNotFounError(Exception):
        pass

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

    class RedisConnectionError(Exception):
        pass
