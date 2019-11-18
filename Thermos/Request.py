from io import BytesIO
import json


class Request:
    """
    Parse a valid HTTP request, returning method, location HTTP version and headers.
    """

    base_http_version = "HTTP/0.9"

    def __init__(self, request=None):
        self.http_version = ""
        self.method = ""
        self.location = ""
        self.headers = {}
        self.body = ""
        self.json = None
        try:
            if request is None:
                raise TypeError("Request not provided")

            if len(request) <= 0:
                raise TypeError("Malformed request")

            request = BytesIO(request)
            request_str = request.readline().decode("utf-8").split()

            # Get method and location from request
            self.method, self.location = request_str[:2]

            # Get HTTP version from request
            self.http_version = request_str[2].split("/")[1]

            while True:
                line = request.readline()
                if len(line) < 1:
                    break
                if line != b"\r\n":
                    line = line.decode("utf-8").split(":", 1)
                    self.headers[line[0].strip()] = line[-1].strip()
                else:
                    line = request.readline().decode("utf-8").strip()
                    if len(line) > 0:
                        self.body = line
                        self.json = json.loads(line)

        except TypeError as err:
            print(err)
