import socket

HOST = "127.0.0.1"   # addr server
PORT = 65432         # server port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = "Hello, server!"
    s.sendall(message.encode())

    data = s.recv(1024)

print("Sent:", message)
print("Received:", data.decode())