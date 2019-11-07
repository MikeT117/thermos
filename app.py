import socket, os
from HttpPackage import HTTPServer

server = HTTPServer.HTTPServer()

while True:
    conn, req = server.conn()

    # Print request to console
    print(
        f"Method: {req.method} - Location: {req.location} - HTTP_Version: {req.http_version}"
    )
    
    @server.Route("/test")
    def test():
        return "Test"

    ### GET ###
    if req.method == "GET":

        # Attempt to retrieve file, if exists return file else return 404
        http_file = server.parse_response_file(req.location.strip("/"))

        # If file is not found return the appropriate response else create a response with the file
        if not http_file:
            resp = server.not_found()
        else:  #
            resp = server.make_response(
                req.http_version, "200", "OK", http_file, req.content_type
            )

        # Send response
        conn.sendall(resp)
        conn.close()
