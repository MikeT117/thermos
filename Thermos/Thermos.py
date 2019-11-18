import socket
from Thermos import (
    make_response,
    not_found,
    parse_file,
    server_error,
    Request,
    MethodNotAllowedError,
    method_not_allowed,
    EmptyMethodsError,
)
from io import BytesIO


class Thermos(object):
    def __init__(
        self,
        port=5000,
        addr="127.0.0.1",
        static_folder="./static/",
        templates_folder="./templates/",
    ):
        try:
            # Check if the user has provided custom settings, if so apply them if not use defaults
            if type(port) is not int:
                raise TypeError("Port must be of type integer.")
            if type(addr) is not str:
                raise TypeError("Address must be of type string.")
            if type(static_folder) is not str:
                raise TypeError("Static folder must be of type string.")
            if type(templates_folder) is not str:
                raise TypeError("Templates folder must of type string")
        except TypeError as err:
            raise

        # Set the default settings.
        self.PORT = port
        self.ADDRESS = addr
        self.STATIC_FOLDER = static_folder
        self.TEMPLATE_FOLDER = templates_folder
        self.routes = {}

    # Starts the request/response loop
    def thermos_run(self):
        # Create the socket
        s = socket.socket()
        # Bind the socket to the address and port
        s.bind((self.ADDRESS, self.PORT))

        # Set the backlog amount
        s.listen(5)

        # Print out thre address and port the server is binded to.
        print(f"Server available at http://{self.ADDRESS}:{self.PORT}")

        # Kickoff the request/response loop
        while True:
            conn = s.accept()[0]
            self.req = Request(conn.recv(4096))
            try:
                ############## GET ################
                if self.req.method == "GET":
                    if len(self.req.location.split(".")) > 1:
                        resp = self.send_static_file(
                            f"{self.STATIC_FOLDER}{self.req.location.strip('/')}"
                        )
                    else:
                        try:
                            resp = self._get_route(self.req.location, self.req.method)
                        except KeyError:
                            resp = not_found()
                        except MethodNotAllowedError:
                            resp = method_not_allowed()

                ##################################

                ############## POST ##############
                if self.req.method == "POST":
                    resp = self._get_route(self.req.location, self.req.method)
                    if not resp:
                        resp = self.send_static_file(
                            f"{self.STATIC_FOLDER}{self.req.location.strip('/')}"
                        )

                ##################################

            except Exception as err:
                print(err)
                resp = server_error()

            finally:
                conn.sendall(resp)
                conn.close()

    # Define a route and add it to the dict
    def route(self, url="/", methods=[]):
        """
        A decorator for defining routes and the methods allowed
        on the route
        """

        if len(methods) < 1:
            raise EmptyMethodsError("Methods cannot be empty")

        def decorator(f):
            self.routes[url] = (f, frozenset(methods))
            return f

        return decorator

    def _get_route(self, route, methods):
        """
        Gets the route based on the location and method from the routes store,
        returns the matching routes function, if no route or a route is found
        but with no matching method an exception is raised and caught in the
        calling function.
        """
        route = self.routes[route]
        if self.req.method in route[1]:
            return route[0](self.req)
        raise MethodNotAllowedError

    # Send a static file to the client - Move to utilities
    def send_static_file(self, filename):
        """
        Sends a file from the static folder to the client
        """
        try:
            # Split filename on '.', and check length is at least 2, return false if not
            split = filename.rsplit(".", 1)
            if len(split) < 2:
                return False

            # Split on 'static' and use the last element, which should always be the filename.
            parsed_file = parse_file(
                f"{self.STATIC_FOLDER}{filename.split('static')[-1]}"
            )
            if not parsed_file:
                return server_error()
            return make_response("1.1", "200", "OK", parsed_file, split[-1])
        except FileNotFoundError as err:
            return not_found()

    def render_template(self, template=None):
        """
        Pulls the 'template' from the template store
        parses it and sends to the client
        """
        try:
            if template is None:
                raise TypeError("Template cannot be empty!")

            if len(template.split(".")) < 2:
                raise KeyError("File extension not provide")

            file = parse_file(f"{self.TEMPLATE_FOLDER}{template}")

            if file:
                return make_response("1.1", "200", "OK", file, "html")

        except (TypeError, KeyError) as err:
            print(err)
            return server_error()
        except FileNotFoundError:
            return not_found()
