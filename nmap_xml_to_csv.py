import nmap
import sys
import optparse
import os

class NmapXMLToCSV:
    def __init__(self) -> None:
        self.filename = self.get_params()

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -f filename' % sys.argv[0])
        parser.add_option('-f', '--filename', dest='filename', type='string', help='Specify filename')
        options, args = parser.parse_args()
        if options.filename is None:
            print(parser.usage)
            sys.exit()
        if not os.path.exists(options.filename):
            print("The file does not exist!")
            sys.exit()
        return options.filename
    
    def run(self):
        nm = nmap.PortScanner()
        with open(self.filename, 'r') as f:
            nm.analyse_nmap_xml_scan(f.read())
            print(nm.csv())
            

if __name__ == '__main__':
    obj = NmapXMLToCSV()
    obj.run()

