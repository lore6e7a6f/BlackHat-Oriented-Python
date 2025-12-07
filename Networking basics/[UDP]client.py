import socket

target, port = "127.0.0.1", 9997
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    n = input("Input to send: ")
    if n == "exit":
        break
    client.sendto(n.encode(), (target, port))
    data, addr = client.recvfrom(4096)
    print(data.decode())
