import os
import sys
import datetime
import platform
import threading

class NetworkScan:
    def __init__(self) -> None:
        if len(sys.argv) < 2:
            self.usage()
            sys.exit()
        
        self.network = sys.argv[1]
        print('Start to scan\n')
        
    
    def usage(self):
        usage = """
            Usage: ./network_scan_by_ping.py network
            Example: ./network_scan_by_ping.py 192.168.84.0
        """
        print(usage)
    
    def ping_host(self,ip):
        oper = platform.system()
        if oper == 'Windows':
            command = 'ping -n 1 %s' % ip
        elif oper == 'Linux':
            command = 'ping -c 1 %s' % ip
        else:
            command = 'ping -c 1 %s' % ip
        response = os.popen(command)
        for line in response.readlines():
            if 'TTL' in line or 'ttl' in line:
                print("%s is alive" % ip)
                break
    
    def run(self):
        start_time = datetime.datetime.now()
        for i in range(1,255):
            ip = self.network.split('.')[0] + '.' + self.network.split('.')[1] + '.' + self.network.split('.')[2] + '.' + str(i)
            t = threading.Thread(target=self.ping_host, args=(ip,))
            t.start()
        end_time = datetime.datetime.now()
        print('\nScan is completed in : %s' % (end_time-start_time))

if __name__ == '__main__':
    scanner = NetworkScan()
    scanner.run()


    