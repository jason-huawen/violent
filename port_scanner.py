import socket
from concurrent.futures import ThreadPoolExecutor
import sys
import ipaddress
import optparse
import queue

class PortScanner:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.ports = self.get_params()[1]
        self.q = queue.Queue()
        self.port_list = []
        if ',' in self.ports:
            for port in self.ports.split(','):
                self.port_list.append(int(port))
        elif '-' in self.ports:
            start_port = self.ports.split('-')[0]
            end_port = self.ports.split('-')[1]
            for port in range(int(start_port), int(end_port)+1):
                self.port_list.append(port)
        else:
            self.port_list.append(int(self.ports))

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target -p port range' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target IP address')
        parser.add_option('-p', '--ports', dest='ports', type='string', help='Specify port range to scan')
        options, args = parser.parse_args()
        if options.ports is None:
            options.ports = '1-1000'
        if options.target is None:
            print('[-] Please specify target IP address')
            sys.exit()
        if not self.check_ip_validity(options.target):
            print('[-] Please specify valide IP address')
            sys.exit()
        return options.target, options.ports
    
    def check_ip_validity(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False
    
    def scan_port(self, port):
        try:
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scan_socket.settimeout(2)
            scan_socket.connect((self.target, port))
            self.q.put(port)
        except:
            pass
    
    def run(self):
        pool = ThreadPoolExecutor(max_workers=5)
        for port in self.port_list:
            pool.submit(self.scan_port,port)
        
        pool.shutdown()
        if self.q.empty():
            print('[-] No open port found on the target: %s' % self.target)
        else:
            print('[-] Port status for the target: %s' % self.target)
            print('\tPort\t\tStatus')
            while not self.q.empty():
                port = self.q.get()
                print('\t%d\t\tOpen' % port)

if __name__ == '__main__':
    scanner = PortScanner()
    scanner.run()