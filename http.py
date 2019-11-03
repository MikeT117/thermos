from io import BytesIO
from datetime import datetime

class HTTPRequest:
    """
    Parse a valid HTTP request, returning method, location HTTP version and headers.
    """

    base_http_version = "HTTP/0.9"

    def __init__(self, request=None):
        self.request = request
        self.http_version = ""
        self.method = ""
        self.location = ""
        self.headers = {}
        try:
            if self.request is None:
                raise TypeError("Request not provided")

            if len(self.request) <= 0:
                raise TypeError("Malformed request")

            self.request = BytesIO(self.request)
            request_str = self.request.readline().decode("utf-8").split()
            self.method, self.location = request_str[:2]

            # Get HTTP version from request
            self.http_version = request_str[2].split("/")[1]

            while True:
                line = self.request.readline().strip()
                if len(line) == 0:
                    break
                decoded = line.decode("utf-8").split(":", 1)
                self.headers[decoded[0]] = decoded[1].strip()

        except TypeError as err:
            print(err)


class HTTPResponse:
    def make_response(
        self,
        http_version,
        status_code,
        status_text,
        data,
        content_type=None,
        headers=None,
    ):
        try:
            if (
                http_version is None
                or status_code is None
                or status_text is None
                or data is None
            ):
                raise TypeError("Malformed response data")
        except Exception as err:
            print(err)

        try:
            if type(data) is not bytes:
                raise TypeError("Data must be bytes")
        except TypeError as err:
            print(err)
            return

        ret = b"HTTP/%b %b %b\n%b\n" % (
            http_version.encode(),
            status_code.encode(),
            status_text.encode(),
            self._content_type(content_type),
        )
        if headers is not None:
            print(headers)
            for i in headers:
                ret += i.encode() + b"\n"
        return ret + b"\n" + data

    def not_found(self):
        return self.make_response(
            "1.1",
            "404",
            "Not Found",
            b"<html><head></head><body><h1>Not found</h1></body></html>",
        )

    def _content_type(self, cType):
        types = {
            "css": b"Content-Type: text/css",
            "html": b"Content-Type: text/html",
            "js": b"Content-Type: text/javascript",
        }

        if cType is None:
            return types["html"]

        cType = cType.split(".")
        if len(cType) != 2:
            return types["html"]

        return types[cType[1]]


def parse_response_file(filename=None):
    try:
        if filename is None:
            raise TypeError("Filename cannot be None")
    except TypeError as err:
        print(err)
        return False
    try:
        if len(filename.split(".")) != 2:
            filename += ".html"

        html_file = open(filename, "rb")
        ret = b""
        while True:
            line = html_file.readline().strip(b" ")
            if len(line) <= 0:
                break
            ret += line
        return ret

    except FileNotFoundError as err:
        print("%s not found" % filename)
        return False
