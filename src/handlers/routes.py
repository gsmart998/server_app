from handlers.handlers import Get, Post, Put, Delete
from logs.my_logging import log


class Routes:
    def __init__(self) -> None:
        self.routes = {}
        self.register_routes()

    def register(self, method: str, path: str, handler: any, auth_check: bool):
        data = {path: {
                "handler": handler,
                "auth_check": auth_check
                }}

        if method in self.routes.keys():
            self.routes[method].update(data)
            return
        self.routes.update({method: data})

    def check_path(self, method, path):
        if path in self.routes[method].keys():
            return True
        return False

    def auth_check(self, method, path):
        return self.routes[method][path]["auth_check"]

    def get_handler(self, method, path):
        return self.routes[method][path]["handler"]

    def get_routes(self):
        result = {}
        for i in self.routes.keys():
            path = []
            for j in self.routes[i].keys():
                path.append(j)
            result[i] = path
        return result

    def register_routes(self):

        self.register("Get", "/todos", Get.todos, True)
        self.register("Post", "/register", Post.register, False)
        self.register("Post", "/login", Post.login, False)
        self.register("Post", "/new", Post.new, True)
        self.register("Post", "/logout", Post.logout, True)
        self.register("Put", "/todo", Put.todo, True)
        self.register("Delete", "/delete", Delete.delete, True)

        log.info(f"Routes registered: {self.get_routes()}")
