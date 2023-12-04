class MyCookie:
    def __init__(self):
        self.uid = None
        self.user_id = None
        self.path = "/"
        self.expire_datetime = None  # store datetime object
        self.expired = None

    def _print(self):
        print("uid:", self.uid)
        print("user_id", self.user_id)
        print("path", self.path)
        print("expire_time", self.expire_datetime)
        print("expired", self.expired)
