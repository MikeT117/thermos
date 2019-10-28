from io import BytesIO


class HTTPRequest:
    def __init__(self, raw_request=None):
        self.request = BytesIO(raw_request)
        self.http_version = "HTTP/0.9"
        self.method = ""
        self.location = "/"
        ## Not sure about calling this from init ##
        self.parse_request()
        self._parse_headers()

    def parse_request(self):
        try:
            if self.request.getbuffer().nbytes <= 0:
                raise TypeError("Request not provided or malformed!")

            # Get method and location from request
            request_list_str = self.request.readline().decode("utf-8").split()
            self.method, self.location = request_list_str[:2]

            # Get HTTP version from request
            http_version = request_list_str[2].split("/")[1].split(".")
            if len(http_version) == 2:
                self.http_version = int(http_version[0]), int(http_version[1])

        except TypeError as err:
            return err

    def _parse_headers(self):
        headers = {}
        while True:
            line = self.request.readline().strip()
            if len(line) == 0:
                break
            headers[line.decode("utf-8").split(":", 1)[0]] = (
                line.decode("utf-8").split(":", 1)[1].strip()
            )
        self.headers = headers
