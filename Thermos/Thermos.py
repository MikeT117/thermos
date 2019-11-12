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

    all_routes = {}

    def __init__(self, port=None, addr=None, static_folder=None, templates_folder=None):

        # Set the default settings.
        self.PORT = 5000
        self.ADDRESS = "127.0.0.1"
        self.STATIC_FOLDER = "./static/"
        self.TEMPLATE_FOLDER = "./templates/"
        self.s = socket.socket()

        # Check if the user has provided custom settings, if so apply them if not use defaults
        if port is not None:
            self.PORT = port
        if addr is not None:
            self.ADDRESS = addr
        if static_folder is not None:
            self.STATIC_FOLDER = static_folder
        if templates_folder is not None:
            self.TEMPLATE_FOLDER = templates_folder

    # Starts the request/response loop
    def thermos_run(self):
        # Bind the socket to the address and port
        self.s.bind((self.ADDRESS, self.PORT))

        # Set the backlog amount
        self.s.listen(5)

        # Print out thre address and port the server is binded to.
        print(f"Server available at http://{self.ADDRESS}:{self.PORT}")

        # Kickoff the request/response loop
        while True:
            conn = self.s.accept()[0]
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
    def route(self, url="/", methods=None):
        """
        A decorator for defining routes and the methods allowed
        on the route
        """
        if methods is None or len(methods) < 1:
            raise EmptyMethodsError("Methods cannot be empty")

        def decorator(f):
            Thermos.all_routes[url] = (f, frozenset(methods))
            return f

        return decorator

    def _get_route(self, route, methods):
        """
        Gets the route based on the location and method from the routes store,
        returns the matching routes function, if no route or a route is found
        but with no matching method an exception is raised and caught in the
        calling function.
        """
        route = self.all_routes[route]
        if self.req.method in route[1]:
            return route[0](self.req)
        raise MethodNotAllowedError

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
                return make_response(self.req.http_version, "200", "OK", file, "html")

        except (TypeError, KeyError) as err:
            print(err)
            return server_error()
        except FileNotFoundError:
            return not_found()

    # Send a static file to the client
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
