import socket
import optparse
import sys

class TCPClient:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        try:
            self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.c_socket.connect((self.target, self.port))
            print('Connected to target: %s' % self.target)
        except Exception as e:
            print('Something is wrong: %s' % e)
            sys.exit()


    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target -p port' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target',type='string', help='Specify target to connect')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port')
        options, args = parser.parse_args()
        if options.target is None or options.port is None:
            print(parser.usage)
            sys.exit()
        return options.target, options.port
    
    def run(self):
        while True:
            data = input("%s# " % self.target)
            if data == 'quit':
                break
            self.c_socket.send(data.encode('utf-8'))
            recv_data = self.c_socket.recv(1024)
            print(recv_data.decode('utf-8'))
    

if __name__ == '__main__':
    client = TCPClient()
    client.run()

    