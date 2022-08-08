import crypt
import sys
import os
import threading
import optparse
import queue

class MyHashCrack:
    def __init__(self) -> None:
        """
        filename: filename of document which wants to be cracked
        wordlist: wordlist used to crack 
        """
        self.filename = self.get_params()[0]
        self.wordlist = self.get_params()[1]
        self.q = queue.Queue()
    
    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -f filename -w wordlist' % sys.argv[0])
        parser.add_option('-f', '--filename', dest='filename', type='string', help='Specify filename to crack')
        parser.add_option('-w', '--wordlist', dest='wordlist', type='string', help='Specify wordlist to crack')
        options, args = parser.parse_args()
        if options.filename is None or options.wordlist is None:
            print(parser.usage)
            sys.exit()
        if not os.path.exists(options.filename):
            print("[-] The file does not exist")
            sys.exit()
        if not os.path.exists(options.wordlist):
            print('[-] The wordlist does not exist')
            sys.exit()
        return options.filename, options.wordlist
    
    def compare_hash_value(self, username, plaintext, salt, hash_value):
        """
        username:
        plaintext:
        salt:
        hash_value:
        """
        try:
            compute_value = crypt.crypt(plaintext,salt)
            if hash_value == compute_value:
                print('[-] Cracked for %s: %s' % (username, plaintext))
                self.q.put(username)

        except:
            pass
    
    def crack_hash(self, username, salt, hash_value):
        f = open(self.wordlist, 'r')
        while True:
            line = f.readline()
            if len(line) == 0:
                break            
         
            t = threading.Thread(target=self.compare_hash_value, args=(username, line.strip(),salt, hash_value))
            t.start()
 

    def run(self):
        """
       $1$/avpfBJ1$x0z8w5UF9Iv./DR9E9Lid.
        """
        with open(self.filename, 'r') as f:
            for line in f.readlines():
            
                username = line.split(':')[0]
                hash_all_info = line.split(':')[1]
         
                if hash_all_info == '*' or hash_all_info == '!':
                    continue
                salt = '$'+ hash_all_info.split('$')[1] +'$' + hash_all_info.split('$')[2] + '$'
                hash_value = hash_all_info.split(':')[-1]   
       
                self.crack_hash(username, salt, hash_value)
        
if __name__ == '__main__':
    cracker = MyHashCrack()
    cracker.run()
        