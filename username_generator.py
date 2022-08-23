import xlrd
import sys
import optparse
import os

class UsernameGenerator:
    def __init__(self) -> None:
        self.filename = self.get_params()[0]
        self.userlist = self.get_params()[1]
        self.users = []

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -f filename -u userlist' % sys.argv[0])
        parser.add_option('-f', '--filename', dest='filename', type='string', help='Specify filename')
        parser.add_option('-u', '--userlist', dest='userlist', type='string', help='Specify userlist to store')
        options, args = parser.parse_args()
        if options.filename is None or options.userlist is None:
            print(parser.usage)
            sys.exit()
        if not os.path.exists(options.filename):
            print("The file does not exist")
            sys.exit()
        return options.filename, options.userlist
    

    def run(self):
        try:
            if os.path.exists(self.userlist):
                print("The userlist has been generated, now exit the program")
                sys.exit()
            else:
                with open(self.userlist, 'w') as f:
                    workbook = xlrd.open_workbook(self.filename)
                    sheet = workbook.sheet_by_index(0)
                    row_number = sheet.nrows
                    for i in range(2,row_number):
                        username = sheet.cell_value(i,0)
                        print(username)
                        self.users.append(username)
                        f.write('%s\n' % username)
                
                
        except Exception as e:
            print(e)
            sys.exit()

if __name__ == "__main__":
    gen = UsernameGenerator()
    gen.run()