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
    