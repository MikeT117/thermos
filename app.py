import socket
from httpRequest import HTTPRequest

s = socket.socket()

port = 5000
s.bind(("", port))
s.listen(5)
print(f"Serving on port: {port}")
while True:
    conn, c_addr = s.accept()
    print(f"Connection from: {c_addr}")

    # Creating HTTP request instance and parsing request
    http_req = HTTPRequest(conn.recv(1024))
    print("Accept: ", http_req.headers["Accept"])
    # Response
    http_resp = b"""\
        HTTP/1.1 200 OK

        Server response!
"""
    conn.sendall(http_resp)
    conn.close()
