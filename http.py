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
        self.content_type = "html"
        try:
            if self.request is None:
                raise TypeError("Request not provided")

            if len(self.request) <= 0:
                raise TypeError("Malformed request")

            self.request = BytesIO(self.request)
            request_str = self.request.readline().decode("utf-8").split()
            self.method, self.location = request_str[:2]

            request_type = self.location.split(".")
            if len(request_type) == 2:
                self.content_type = request_type[1]

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


def make_response(
    http_version, status_code, status_text, data, content_type, headers=None
):
    try:
        if (
            http_version is None
            or status_code is None
            or status_text is None
            or data is None
        ):
            raise TypeError("Malformed response data")

        if type(data) is not bytes:
            raise TypeError("Data must be bytes")
    except TypeError as err:
        print(err)
        return False

    # Determining content type, Defaults to HTML
    content_types = {
        "css": b"Content-Type: text/css",
        "html": b"Content-Type: text/html",
        "js": b"Content-Type: application/javascript",
        "jpg": b"Content-Type: image/jpg",
        "jpeg": b"Content-Type: image/jpeg",
        "gif": b"Content-Type: image/gif",
        "png": b"Content-Type: image/png",
        "jpg": b"Content-Type: image/jpg",
        "ico": b"Content-Type: image/ico",
    }

    # Set 'Content-Type' header based on extension, return html as default
    if content_type is None:
        content_type = content_types["html"]
    else:
        content_type = content_types[content_type]

    # Return response
    ret = b"HTTP/%b %b %b\n%b\n" % (
        http_version.encode(),
        status_code.encode(),
        status_text.encode(),
        content_type,
    )

    # Parse additional headers and add to response
    if headers is not None:
        for i in headers:
            ret += i.encode() + b"\n"
    return ret + b"\n" + data


# Not found response, 404
def not_found():
    return make_response(
        "1.1",
        "404",
        "Not Found",
        b"<html><head></head><body><h1>404: Not found</h1></body></html>",
        "html",
    )


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
            if filename.split(".")[1] in {"jpg", "png", "jpeg", "gif", "ico"}:
                line = html_file.readline()
            else:
                line = html_file.readline().strip(b" ")
            if len(line) <= 0:
                break
            ret += line
        return ret

    except FileNotFoundError as err:
        print("%s not found" % filename)
        return False
