import socket
import subprocess
import threading
import sys
import optparse
import shlex

class Server:
    def __init__(self,port) -> None:
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0',self.port))
        self.server_socket.listen(5)
        self.banner = """
            Welcome to use net tool by Jason Huawen version 1.0.0
        """
    
    def client_handler(self, client_socket, client_addr):
        print("[+] Connected from : %s %d" % (client_addr[0], client_addr[1]))
        client_socket.send(self.banner.encode('utf-8'))
        while True:
            command = input("%s $ " % client_addr[0])
            if command.strip() == 'quit':
                break
            client_socket.send(command.encode('utf-8'))
            data_recv = client_socket.recv(1024)
            print(data_recv.decode('utf-8'))


    def run(self):
        while True:
            client_socket, client_addr = self.server_socket.accept()
            t = threading.Thread(target=self.client_handler, args=(client_socket, client_addr))
            t.start()

class Client:
    def __init__(self,target, port) -> None:
        self.target = target
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            self.client_socket.connect((self.target, self.port))
        except Exception as e:
            print("[-] Failed to connect to back: %s" % e)
            sys.exit()

    def run(self):
        banner = self.client_socket.recv(1024)
        print(banner.decode('utf-8'))
        while True:
            command = self.client_socket.recv(1024)
            if command:
                if command.decode('utf-8').strip() == 'quit':
                    break
                else:
                    result = subprocess.check_output(shlex.split(command.decode('utf-8')), stderr=subprocess.STDOUT)
                    self.client_socket.send(result)

if __name__ == '__main__':
    parser = optparse.OptionParser('Usage:./%s -t IP address -l -p port' % sys.argv[0])
    parser.add_option('-t', '--target',action='store',dest='target', type='string', help='Specify IP address')
    parser.add_option('-l','--mode', action='store_true', dest='mode', help='Specify mode')
    parser.add_option('-p', '--port', dest='port', type='int', help='Specify port number' )
    options, args = parser.parse_args()
    if options.target:
        target_addr = options.target
    port = int(options.port)
    if options.mode is None:
        print("Client mode")
        client = Client(target_addr, port)
        client.run()
    else:
        print("Server mode")
        server = Server(port)
        server.run()
