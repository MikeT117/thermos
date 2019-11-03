import socket, os
from http import HTTPRequest, HTTPResponse, parse_response_file

PORT = int(os.environ.get("http_server_port", 5000))
ADDRESS = os.environ.get("http_server_address", "127.0.0.1")

s = socket.socket()
s.bind((ADDRESS, PORT))
s.listen(5)

print(f"Server available at http://{ADDRESS}:{PORT}")

while True:
    conn, c_addr = s.accept()

    # Creating HTTP request instance and parsing request
    request = HTTPRequest(conn.recv(1024))

    # Print request to console
    print(
        f"Method: {request.method} - Location: {request.location} - HTTP_Version: {request.http_version}"
    )

    ### GET ###
    if request.method == "GET":
        # Attempt to retrieve file, if exists return file else return 404
        http_file = parse_response_file(request.location.strip("/"))
        if not http_file:
            http_resp = HTTPResponse()
            resp = http_resp.not_found()
        else:  #
            http_resp = HTTPResponse()
            resp = http_resp.make_response(
                request.http_version, "200", "OK", http_file, request.location
            )
        print("RESP: ", resp)
        # Send response
        conn.sendall(resp)
        conn.close()
