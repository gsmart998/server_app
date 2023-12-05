from http_.handlers.post import Post
from http_.handlers.delete import Delete
from http_.handlers.put import Put
from http_.handlers.get import Get
from logs.my_logging import log
from http_.router.router import Router

routes = Router()


def register_routes():

    routes.register("Get", "/todos", Get.todos)
    routes.register("Post", "/register", Post.register)
    routes.register("Post", "/login", Post.login)
    routes.register("Post", "/new", Post.new)
    routes.register("Post", "/logout", Post.logout)
    routes.register("Put", "/todo", Put.todo)
    routes.register("Delete", "/delete", Delete.delete)

    log.info(f"Routes registered: {routes.get_routes()}")
