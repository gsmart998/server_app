from http import cookies
import json

from jsonschema import ValidationError, validate

from logs.my_logging import log
from jsonschema.exceptions import ValidationError


class ParseErorr(Exception):
    pass


class Request():
    """
    Class for processing incoming requests.
    Reads, parses, and allows you to generate a response.
    """

    def read(self) -> tuple:
        """
        Read recived request for cookie uid. return uid, user_id.
        If cookie doesn't contain uid and user_id - return None, None
        """
        cookie = self.headers.get('Cookie')
        if cookie != None:
            # try to find uid index in cookie
            # if r = -1 'uid=' doesn't exist, then uid = None
            r = cookie.find("uid=")
            r2 = cookie.find(":id=")
            if r != -1 and r2 != -1:
                uid = cookie[r+5:r2]  # fetch uid from cookie
                user_id = cookie[r2 + 4:-1]  # fetch user id from cookie
                return uid, user_id

        return None, None

    def parse(self, template: dict) -> dict:
        """
        Parse method receive a json and shema template,
        check it for correctness and convert it into a
        dictionary, then return body as dict.
        """
        # Getting the length of the request body
        content_length = int(self.headers["Content-Length"])

        # Receiving the request body
        body = self.rfile.read(content_length)
        try:
            body = json.loads(body)  # Convert it to a dictionary
        except json.JSONDecodeError as e:
            log.error("'parse' Error while reading json file. Error'{e}'")
            raise ParseErorr("Error while reading json file. Error'{e}'")

        # Validation of JSON file fields
        try:
            validate(body, template)

        except ValidationError as e:
            log.error(f"'parse' Json is not valid! Error'{e}'")
            raise ParseErorr(f"Json is not valid! Error'{e}'")

        return body

    def respond(self, code: int, text: str, uid: str = None, user_id: int = None):
        """
        Respond method takes as input a response code, a json file,
        and optionally a uid and user id, and sends the generated data in
        response to request.
        """
        json_ok = {
            "status": "Ok",
            "message": text
        }
        json_err = {
            "status": "Error",
            "error_code": code,
            "message": text
        }

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        if uid != None and user_id != None:
            new_cookie = cookies.SimpleCookie()
            new_cookie["uid"] = f"{uid}:id={user_id}"
            new_cookie["uid"]["path"] = "/"
            new_cookie["uid"]["HttpOnly"] = True

            self.send_header("Set-Cookie", new_cookie.output(header=''))
        self.end_headers()

        if code == 200:
            respond = json.dumps(json_ok)
        else:
            respond = json.dumps(json_err)

        self.wfile.write(bytes(respond, "UTF-8"))
        log.info(f"Respond sent with code: '{code}'.")
