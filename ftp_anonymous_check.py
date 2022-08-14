import ftplib
import sys
import optparse
import socket


class FTPAnonymousCheck:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target IP address -p port' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target IP address')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port')
        options, args = parser.parse_args()
        if options.target is None:
            print(parser.usage)
            sys.exit()
        if options.port is None:
            options.port = 21
        return options.target, options.port
    
    def check_ftp_status(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.target, self.port))
            return True
        except:
            print("No FTP service running over the port of target: %s" % self.target)
            return False
    
    def run(self):
        if self.check_ftp_status():
            ftp = ftplib.FTP(host=self.target)
            try:
                ftp.connect(host=self.target,port=self.port)
                ftp.login('anonymous', 'test@163.com')
                print('The target allows anonynous login: %s' % self.target)
                ftp.quit()
            except:
                print('The target does not allow anonynmous login: %s' % self.target)
                sys.exit()

if __name__ == '__main__':
    checker = FTPAnonymousCheck()
    checker.run()