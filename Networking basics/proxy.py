import sys, socket, threading

HEX_FILTER = ''.join([len(repr(chr(i)))==3] and chr(i) or '.' for i in range(256))

def hex_dump(src, lenght=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()
    for i in range(0, len(src), lenght):
        word = str(src[i:i+lenght])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexawidth = lenght*3
        results.append(f'{i:04x} {hexa:<{hexawidth}} {printable}') #joining everything

    if show:
        for line in results:
            print(line)
    else:
        return results
    
def receive_from(connection):
    bufffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data  
    except Exception as e:
        pass

    return buffer

def request_handler(buffer):
    # frame tuning
    return buffer

def response_handler(buffer):
    # frame tuning
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hex_dump(remote_buffer)

    # remote_buffer = response_handler(remote_buffer) not usefull yet

    if len(remote_buffer):
        print("[==>] Sending %d bytes from localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:

        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            line = "[<==] Received %d bytes from localhost." & len(local_buffer)
            print(line)
            hex_dump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." & len(remote_buffer))
            hex_dump(remote_buffer)
            
            # remote_buffer = response_handler(remote_buffer) not usefull yet
            remote_socket.send(remote_buffer)
            print("[==>] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[!] No more data, closing connections...")
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print('Problem on bind: %o' %e)
        print('[!] Failed to listen on %s:%d' %(local_host, local_port))
        sys.exit()

    print('[*] Listening on %s:%d' %(local_host, local_port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        line = "> Received incoming connection from %s:%d" (addr[0], addr[1])
        print(line)

        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )

        proxy_thread.start()

def main():
    if len(sys.argv[1:] != 5):
        print("Usage: ,/proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit()

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]
    if True in recieve_first:
        recieve_first = True
    else:
        recieve_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == "__main__":
    main()


