import zipfile
import sys
import optparse
import os
from concurrent.futures import ThreadPoolExecutor   # Use thread pool to speed brute force attack
import queue



class MyZIPCracker:
    def __init__(self) -> None:
        """
        filename: filename of the file which will be cracked
        wordlist: filename or filepath of the wordlist which will be used as dictionary
        q: queue instance to store data between different threads
        """

        self.filename = self.get_params()[0]
        self.wordlist = self.get_params()[1]
        self.q = queue.Queue()
        try:
            self.zipper = zipfile.ZipFile(self.filename)
            print('[-] Begin to crack the encrypted file!')
        except Exception as e:
            print('[-] Failed to start cracking: %s' % e)
            sys.exit()

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -f filename -w wordlist' % sys.argv[0])
        parser.add_option('-f', '--filename', dest='filename', type='string', help='Specify filename to crack')
        parser.add_option('-w', '--wordlist', dest='wordlist', type='string', help='Specify wordlist path')
        options, args = parser.parse_args()
        if options.filename is None or options.wordlist is None:
            print('[-]', parser.usage)
            sys.exit()
        if not os.path.exists(options.filename):
            print('[-] The file does not exist')
            sys.exit()
        if not os.path.exists(options.wordlist):
            print('[-] The wordlist does not exist')
            sys.exit()
        return options.filename, options.wordlist
    
    def open_file(self,password):
        try:
            self.zipper.extractall(pwd=password.encode('utf-8'))   # Notes: pwd should be encoded ant passed to the extractall method
            print('[-] Password Found: %s' % password)
            self.q.put(password)     # When found the password, which will be saved into self.q. This can be control signal to prevent to generate more threads
        except:
            pass
    
    def run(self):
        pool = ThreadPoolExecutor(max_workers=5)
        with open(self.wordlist) as f:
            while True:
                try:
                    line = f.readline()      # When open big wordlist, some error will happen . This error or exception should be catched.
                except:
                    pass
                if len(line) ==0:            # When the file pointer goes to the end of the file, break the loop
                    break
                if not self.q.empty():       # When self.q is not empty, it means that the password has been found without needing to go on cracking
                    break
                if self.q.empty():
                    pool.submit(self.open_file,line.strip())
              
        

if __name__ == '__main__':
    cracker = MyZIPCracker()
    cracker.run()   