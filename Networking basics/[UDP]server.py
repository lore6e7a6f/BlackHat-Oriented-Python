import socket

ip = "0.0.0.0"
port = 9997

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((ip, port))

print(f"UDP server listening on {ip}:{port}")

while True:
    data, addr = server.recvfrom(1024)
    print(f"Received from {addr}: {data.decode()}")
    server.sendto(b"ok", addr)
