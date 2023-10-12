from jsonschema import ValidationError, validate
from my_logging import log


# Register template
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

# Auth template
login_schema = {
    "type": "object",
    "properties": {
        "login": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["login", "password"],
    "additionalProperties": False
}

# Template for new todo
new_todo_schema = {
    "type": "object",
    "properties": {
        "task": {"type": "string"},
        "completed": {"type": "number"}
    },
    "required": ["task", "completed"],
    "additionalProperties": False
}

# Template for update todo
update_todo_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "task": {"type": "string"},
        "completed": {"type": "number"}
    },
    "required": ["id", "task", "completed"],
    "additionalProperties": False
}

delete_todo_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"}
    },
    "required": ["id"],
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

    elif path == "/new":
        try:
            validate(body, new_todo_schema)
        except ValidationError as e:
            return f"Json is not valid! Error'{e}'"

    elif path == "/todo":
        try:
            validate(body, update_todo_schema)
        except ValidationError as e:
            return f"Json is not valid! Error'{e}'"

    elif path == "/delete":
        try:
            validate(body, delete_todo_schema)
        except ValidationError as e:
            return f"Json is not valid! Error'{e}'"

    else:
        error = "json_validate, invalid path/schema!"
        return error
