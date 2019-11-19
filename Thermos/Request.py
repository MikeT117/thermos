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

            # Begin parsing headers and JSON is present
            while True:
                # Read a line from the request (reads until /r or .n is hit)
                line = request.readline()

                # Checks if line length is more than 1, if not break the loop
                if len(line) < 1:
                    break
                # If line does not contain (only) '\r\n' add the header name and value to the list
                if line != b"\r\n":
                    line = line.decode("utf-8").split(":", 1)
                    self.headers[line[0].strip()] = line[-1].strip()
                # If line does contain '\r\n' (signalling the beginnning of the request body) read another
                # if line length is more than 0 save it in the body variable and parse the body variable from json
                else:
                    line = request.readline().decode("utf-8").strip()
                    if len(line) > 0:
                        self.body = line
                        self.json = json.loads(line)

        except TypeError as err:
            print(err)
