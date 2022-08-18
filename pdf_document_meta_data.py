import pikepdf
import sys
import os
import optparse

class PDFDocumentMeta:
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
            print('The file does not exist!')
            sys.exit()
        return options.filename
    

    def run(self):
        try:
            pdf = pikepdf.Pdf.open(self.filename)
            docinfo = pdf.docinfo
            print("The meta inforamtion about the file: %s" % self.filename)
            for k, v in docinfo.items():
                if k.startswith('/'):
                    k = k.lstrip('/')
            
                print(k, "\t", v)
        except Exception as e:
            print("Something is wrong: %s" % e)
            sys.exit()

if __name__ == '__main__':
    pdf = PDFDocumentMeta()
    pdf.run()

        
        