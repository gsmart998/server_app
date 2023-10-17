from http import cookies
import json
from my_logging import log

from email_validator import ValidatedEmail
import schema_template as schema
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
        Read recived request for path '/some_path' and
        cookie uid. return (uid, path)
        """
        cookie = self.headers.get('Cookie')
        uid = cookie[cookie.index('=') + 1:]  # fetch uid from cookie
        path = self.path
        return (uid, path)

    def parse(self, path: str) -> dict:
        """
        Parse method receive a json and path string,
        check it for correctness and convert it into a
        dictionary, then return body as dict.
        """
        # Getting the length of the request body
        content_length = int(self.headers["Content-Length"])

        # Receiving the request body
        body = self.rfile.read(content_length)
        try:
            body = json.loads(body)  # Convert it to a dictionary
        except json.JSONDecodeError:
            log.error("Error while reading json file.")
            raise ParseErorr("Error while reading json file.")
        # Validation of JSON file fields
        try:
            schema.json_validate(body, path)
        except ValidationError as e:
            log.error(f"Json is not valid! Error'{e}'")
            raise ParseErorr(f"Json is not valid! Error'{e}'")

        return body

    def respond(self, code: int, json: str, cookie: str = None):
        """
        Respond method takes as input a response code, a json file,
        and optionally a cookie, and sends the generated data in
        response to request.
        """
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        if cookie != None:
            new_cookie = cookies.SimpleCookie()
            new_cookie["uid"] = cookie
            new_cookie["uid"]["path"] = "/"
            new_cookie["uid"]["HttpOnly"] = True

            self.send_header("Set-Cookie", new_cookie.output(header=''))
        self.end_headers()
        self.wfile.write(bytes(json, "UTF-8"))
        log.info(f"Respdond sent with code: '{code}'.")
