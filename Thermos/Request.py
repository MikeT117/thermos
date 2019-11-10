from io import BytesIO


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
        self.content_type = "html"
        try:
            if request is None:
                raise TypeError("Request not provided")

            if len(request) <= 0:
                print(request)
                raise TypeError("Malformed request")

            request = BytesIO(request)
            request_string = request.readline().decode("utf-8").split()
            self.method, self.location = request_string[:2]

            request_type = self.location.split(".")
            if len(request_type) == 2:
                self.content_type = request_type[1]

            # Get HTTP version from request
            self.http_version = request_string[2].split("/")[1]

            while True:
                line = request.readline().strip()
                if len(line) == 0:
                    break
                decoded = line.decode("utf-8").split(":", 1)
                self.headers[decoded[0]] = decoded[1].strip()

        except TypeError as err:
            print(err)
