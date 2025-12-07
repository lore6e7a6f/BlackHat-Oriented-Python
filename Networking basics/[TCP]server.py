import socket, threading

ip = '0.0.0.0'
port = 9997

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    print(f"Listening on {port} : {ip}")

    while True:
        client, address = server.accept()
        print(f"Accepted connession from {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
         while True:
            data = sock.recv(1024)
            if data.decode() == "exit":
                break   # client closed connection
            
            print(f"Received: {data.decode('UTF-8')}")
            sock.send(b'ok')

if __name__ == "__main__":
    main()