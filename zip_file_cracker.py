import zipfile
import sys
import optparse
import os
from concurrent.futures import ThreadPoolExecutor
import queue



class MyZIPCracker:
    def __init__(self) -> None:
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
            self.zipper.extractall(pwd=password.encode('utf-8'))
            print('[-] Password Found: %s' % password)
            self.q.put(password)
        except:
            pass
    
    def run(self):
        pool = ThreadPoolExecutor(max_workers=5)
        with open(self.wordlist) as f:
            while True:
                try:
                    line = f.readline()
                except:
                    pass
                if len(line) ==0:
                    break
                if not self.q.empty():
                    break
                if self.q.empty():
                    pool.submit(self.open_file,line.strip())
              
        

if __name__ == '__main__':
    cracker = MyZIPCracker()
    cracker.run()   