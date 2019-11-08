import socket
from io import BytesIO


class Thermos(object):

    all_routes = {}

    def __init__(self, port=None, addr=None, static_folder=None):

        # Set the default settings.
        self.PORT = 5000
        self.ADDRESS = "127.0.0.1"
        self.STATIC_FOLDER = "./static/"
        # Instantiate the socket
        self.s = socket.socket()

        # Check if the user has provided custom settings, if so apply them if not use defaults
        if port is not None:
            self.PORT = port
        if addr is not None:
            self.ADDRESS = addr
        if static_folder is not None:
            self.STATIC_FOLDER = static_folder

    # Starts the request/response loop
    def initialise_server(self):
        # Bind the socket to the address and port
        self.s.bind((self.ADDRESS, self.PORT))

        # Set the backlog amount
        self.s.listen(5)

        # Print out thre address and port the server is binded to.
        print(f"Server available at http://{self.ADDRESS}:{self.PORT}")
        # Kickoff the request/response loop
        while True:
            self.conn = self.s.accept()[0]
            self.req = Request(self.conn.recv(1024))

            if len(self.req.location.split(".")) == 2 and self.req.location.split(".")[
                1
            ] in {"css", "jpg", "png", "jpeg", "js"}:
                resp = self.parse_response_file(
                    f"{self.STATIC_FOLDER}{self.req.location.strip('/')}"
                )
                if resp:
                    self.conn.sendall(resp)
                    self.conn.close()
            elif self.req.method == "GET":
                try:
                    resp = Thermos.all_routes[self.req.location](self.req)
                except Exception as err:
                    resp = not_found()
                finally:
                    self.conn.sendall(resp)
                    self.conn.close()

            elif self.req.method == "POST":
                pass

    # Define a route and add it to the dict
    def route(self, url="/"):
        def decorator(f):
            Thermos.all_routes[url] = f
            return f

        return decorator

    def parse_response_file(self, filename=None):
        print("FILENAME: ", filename)
        try:
            if filename is None:
                raise TypeError("Filename cannot be None")
        except TypeError as err:
            print(err)
            return False

        try:
            if len(filename.split(".")) < 2:
                filename += ".html"
            if filename.rsplit(".", 1)[1] in {
                "jpg",
                "png",
                "jpeg",
                "gif",
                "ico",
                "css",
                "js",
            }:
                html_file = open(filename, "rb")
            else:
                html_file = open(f"{self.STATIC_FOLDER}{filename}", "rb")
            ret = b""
            while True:
                if filename.rsplit(".", 1)[1] in {"jpg", "png", "jpeg", "gif", "ico"}:
                    line = html_file.readline()
                else:
                    line = html_file.readline().strip(b" ")
                if len(line) <= 0:
                    break
                ret += line
            return ret

        except FileNotFoundError as err:
            print(err)
            print("%s not found" % filename)
            # Return false in which case the client will be sent a 404
            return False


class Request:
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
                print(self.request)
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


def not_found():
    return make_response(
        "1.1",
        "404",
        "Not Found",
        b"<html><head></head><body><h1>404: Not found</h1></body></html>",
        "html",
    )


def send_static_file(filename):
    pass
