import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return ''
    try:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ""
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                
                if response:
                    print(response, end='')
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("\nTerminated.")
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f"Listening on {self.args.target}:{self.args.port} ...")
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            output = f"Saved file {self.args.upload}\n"
            client_socket.send(output.encode())
        elif self.args.command:
            cmd_buffer = b''
            try:
                while True:
                    client_socket.send(b'server: #> ')
                    while b'\n' not in cmd_buffer:
                        cmd_buffer += client_socket.recv(4096)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
            except Exception as e:
                print(f"Server killed {e}")
                self.socket.close()
                sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='My NetCat',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Example:
        netcat.py -t <ip> -p <port>
        netcat.py -t <ip> -p <port> -c
        netcat.py -t <ip> -p <port> -l -u=<myfile.extension>
        netcat.py -t <ip> -p <port> -l -e="cat /etc/passwd"
        echo 'Hi' | ./netcat.py -t <ip> -p <port> 
        """)
    )
    
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='executes specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='specified IP')
    parser.add_argument('-u', '--upload', help='uploads file')

    args = parser.parse_args()

    if args.listen:
        buffer = b''
    else:
        buffer = sys.stdin.read().encode()

    nc = NetCat(args, buffer)
    nc.run()
