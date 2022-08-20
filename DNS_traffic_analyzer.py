from scapy.all import *
import sys
import optparse


class DNSTrafficAnalyzer:
    def __init__(self) -> None:
        self.interface = self.get_params()
        self.DNSRecords = {}

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -i interface' % sys.argv[0])
        parser.add_option('-i', '--interface', dest='interface', type='string', help='Specify interface to monitor')
        options, args = parser.parse_args()
        if options.interface is None:
            print(parser.usage)
            sys.exit()
        return options.interface
    
    def packet_handler(self, pkt):
        if pkt.haslayer(DNSRR):
            rrname = pkt.getlayer(DNSRR).rrname.decode('utf-8')
            rdata = pkt.getlayer(DNSRR).rdata.decode('urf-8')
            if rrname in self.DNSRecords.keys():
                if rdata not in self.DNSRecords[rrname]:
                    self.DNSRecords[rrname].append(rdata)
                    print(rrname, rdata)
            else:
                self.DNSRecords[rrname]=[]
                self.DNSRecords[rrname].append(rdata)        
                print(rrname, rdata)  
          

    
    def run(self):
        try:
            sniff(iface=self.interface, store=0, prn=self.packet_handler)
        except KeyboardInterrupt:
            print('Exiting the program now!')
            sys.exit()
        except Exception as e:
            print(e)
            sys.exit()


if __name__ == '__main__':
    analyzer = DNSTrafficAnalyzer()
    analyzer.run()