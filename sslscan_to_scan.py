import subprocess
import optparse
import sys
import socket

class SSLScanner:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = int(self.get_params()[1])

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target -p port' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify host')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port to scan')
        options, args = parser.parse_args()
        if options.port is None:
            options.port = 443
        if options.target is None:
            print("Please specify target to scan")
            sys.exit()
        return options.target, options.port
    
    def check_port_status(self):
        try:
            c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c_socket.settimeout(2)
            c_socket.connect((self.target, self.port))
        except Exception as e:
            print("The port is unreachable", e)
            sys.exit()
    
    def run(self):
        self.check_port_status()        
        command = "sslscan %s:%d" % (self.target, self.port)
        result = subprocess.check_output(command.split())

        if result:
            with open('scan_result.csv', 'w') as f:
                result = result.decode('utf-8')
                for line in result.splitlines():
                    if 'Accepted' in line:
                        # print('='*100)
                        f.write('%s,%s,%s\n'%(line.split()[1],line.split()[2],line.split()[3]))
                        # f.write(line.split()[1],',', line.split()[2],',',line.split()[3],'\r')                
        else:
            print("Failed to scan")

if __name__ == '__main__':
    scanner = SSLScanner()
    scanner.run()
