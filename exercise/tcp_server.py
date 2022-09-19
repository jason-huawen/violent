import socket
import sys
import optparse
import threading


class TCPServer:
    def __init__(self) -> None:
       
        self.port = self.get_params()
        try:
            self.s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s_socket.bind(('0.0.0.0', self.port))
            self.s_socket.listen(5)            
            print('Start to listen on port:  %d' % self.port)
        except Exception as e:
            print('Something is wrong: %s' % e)
            sys.exit()


    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s  -p port' % sys.argv[0])        
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port')
        options, args = parser.parse_args()
        if options.port is None:
            print(parser.usage)
            sys.exit()
        return options.port
    
    def client_process(self,c_socket, c_address):
        print("%s connected successfully" % c_address[0])
        while True:
            recv_data = c_socket.recv(1024)
            if len(recv_data) == 0:
                break
            print(recv_data.decode('utf-8'))
            send_data = input('Input data to send: ')
            c_socket.send(send_data.encode('utf-8'))
            

    
    def run(self):
        while True:
            c_socket, c_address = self.s_socket.accept()
            t = threading.Thread(target=self.client_process, args=(c_socket, c_address))
            t.start()

if __name__ == '__main__':
    tcpserver = TCPServer()
    tcpserver.run()
