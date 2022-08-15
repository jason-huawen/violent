import ftplib
import optparse
import sys

class FTPWebFileFinder:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        self.username = self.get_params()[2]
        self.password = self.get_params()[3]
        self.ftp  = ftplib.FTP(host=self.target)

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target IP address -p port -u username -P passowrd' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target IP address')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port')
        parser.add_option('-u', '--username', dest='username', type='string', help='Specify username')
        parser.add_option('-P', '--password', dest='password', type='string', help='Specify password')
        options, args = parser.parse_args()
        if options.target is None:
            print(parser.usage)
            sys.exit()

        if options.port is None:
            options.port = 21
   
        if options.username is None or options.password is None:
            print('Specify username or password')
            sys.exit()

        return options.target, options.port, options.username, options.password
    
    def ftp_login(self):
        try:
            
            self.ftp.connect(host=self.target, port=self.port)
            self.ftp.login(user=self.username, passwd=self.password)           
            
        except Exception as e:
            print('[-] Failed to login to target: %s' % e)
            sys.exit()
    
    def list_files(self):
        try:
            dir_list = self.ftp.nlst()
            if len(dir_list)==0:
                return "No files or directories returned"
            return dir_list
        except:
            return "Falied to return files"
    
    def find_web_documents(self):
        self.ftp_login()
        dir_list = self.list_files()
        if dir_list == "No files or directories returned":
            print("No files or directories returned")
        elif dir_list == "Falied to return files":
            print("Falied to return files")
        else:
            print('The target has the following files: \n')
            for item in dir_list:
                print('\t', item)

if __name__ == '__main__':
    finder = FTPWebFileFinder()
    finder.find_web_documents()
