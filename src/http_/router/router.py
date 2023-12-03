class Router:
    routes = {}

    def register(self, method: str, path: str, handler: any):
        data = {
            path: {"handler": handler}
        }

        if method in self.routes.keys():
            self.routes[method].update(data)
            return
        self.routes.update({method: data})

    def check_path(self, method, path):
        if path in self.routes[method].keys():
            return True
        return False

    # def auth_check(self, method, path):
    #     return self.routes[method][path]["auth_check"]

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
