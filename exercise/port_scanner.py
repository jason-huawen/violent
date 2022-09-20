import socket
import threading
import sys


class MyPortScanner:
    def __init__(self) -> None:
        if len(sys.argv) < 3:
            self.usage()
            sys.exit()
        
        self.target = sys.argv[1]
        self.port_range = sys.argv[2]
        self.port_list = self.port_info_process()
        print('Start to scan......')
            

    def usage(self):
        usage = """
            Usage:
                 ./port_scanner.py ip_address port_range
        """
        print(usage)
    
    def port_info_process(self):
        port_list = []
        if ',' in self.port_range:
            port_list = [int(x) for x in self.port_range.split(',') ]

        elif '-' in self.port_range:
            start_port = self.port_range.split('-')[0]
            end_port = self.port_range.split('-')[1]
            for port in range(int(start_port),int(end_port)):
                port_list.append(port)

        else:
            port_list.append(int(self.port_range))
        
        return port_list
    
    def port_scan(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        response = s.connect_ex((self.target,port))
        if not response:
            print('Port %d open' % port)
    
    def run(self):
        for port in self.port_list:
            t = threading.Thread(target=self.port_scan, args=(port,))
            t.start()


if __name__ == '__main__':
    scanner = MyPortScanner()
    scanner.run()


