import socket

s = socket.socket()
host = socket.gethostname()
port = 5000
s.connect((host, port))
print("Details: ", s.getpeername(), s.getsockname())
print("Received Message: ", s.recv(1024).decode('utf-8'))
s.close()