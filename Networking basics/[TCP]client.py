import socket

target = '127.0.0.1'
port = 9997

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target, port))

while True:
    
    n=input(str("Input to send: "))
    if n=="exit":
        break
    else:
        client.send(n.encode())
        r = client.recv(4096)
        print(r.decode())
