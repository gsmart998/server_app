from jsonschema import ValidationError, validate
from my_logging import log


# Шаблон json файла формы регистрации
register_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "login": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string"},
    },
    "required": ["name", "login", "password", "email"],
    "additionalProperties": False
}

# Шаблон json файла формы авторизации
login_schema = {
    "type": "object",
    "properties": {
        "login": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["login", "password"],
    "additionalProperties": False
}


def json_validate(body, path: str):
    """
    Function takes as input a dictionary and the path name
    for checking. Returns an error if encountered.
    """

    if path == "/register":
        try:
            validate(body, register_schema)
        except ValidationError as e:
            return f"Json is not valid! Error'{e}'"

    elif path == "/login":
        try:
            validate(body, login_schema)
        except ValidationError as e:
            return f"Json is not valid! Error'{e}'"
    else:
        error = "json_validate, invalid path/schema!"
        return error
