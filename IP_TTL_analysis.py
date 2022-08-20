from scapy.all import *
import sys
import optparse

class TTLAnalyzer:
    def __init__(self) -> None:
        self.interface = self.get_params()

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -i interface' % sys.argv[0])
        parser.add_option('-i', '--interface', dest='interface', type='string', help='Specify interface to monitor')
        options, args = parser.parse_args()
        if options.interface is None:
            print(parser.usage)
            sys.exit()
        return options.interface
    
    def packet_handler(self, pkt):
        try:
            if pkt.haslayer(IP):
                ttl = str(pkt.getlayer(IP).ttl)
                print('TTL Value from %s: %s' % (pkt.getlayer(IP).src, ttl))
        except:
            pass

    def run(self):
        try:
            sniff(prn=self.packet_handler, store=0,iface=self.interface)
        except KeyboardInterrupt:
            print('Exiting the program')
            sys.exit()
        except Exception as e:
            print('Something is wrong: %s' % e)
            sys.exit()

if __name__ == '__main__':
    analyzer = TTLAnalyzer()
    analyzer.run()