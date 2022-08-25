import requests
import sys
import os
import optparse
from concurrent.futures import ThreadPoolExecutor

class DirectoryEnumerate:
    def __init__(self) -> None:
        self.url = self.suffix_url(self.get_params()[0])
        self.wordlist = self.get_params()[1]
        self.header = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
        }
        banner = """


                ____.                             __      __                      
                |    |____    __________   ____   /  \    /  \____   ____    ____  
                |    \__  \  /  ___/  _ \ /    \  \   \/\/   /  _ \ /    \  / ___\ 
            /\__|    |/ __ \_\___ (  <_> )   |  \  \        (  <_> )   |  \/ /_/  >
            \________(____  /____  >____/|___|  /   \__/\  / \____/|___|  /\___  / 
                        \/     \/           \/         \/             \//_____/  



                       Directory Enumerate Tool V1.0

        """
        print(banner)

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -u url -w wordlist' % sys.argv[0])
        parser.add_option('-u', '--url', dest='url', type='string', help='Specify url to enumerate')
        parser.add_option('-w', '--wordlist', dest='wordlist', type='string', help='Specify wordlist')
        options, args = parser.parse_args()
        if options.url is None or options.wordlist is None:
            print(parser.usage)
            sys.exit()
        if not os.path.exists(options.wordlist):
            print('The wordlist does not exist!')
            sys.exit()
        return options.url, options.wordlist
    
    def suffix_url(self,url):
        if url.endswith('/'):
            return url
        else:
            return url+'/'
    
    def check_url_status(self):
        try:
            response = requests.get(url=self.url, headers=self.header)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
    def req_generator(self, url):
        try:
            response = requests.get(url=url, headers=self.header)
            if response.status_code == 200:
                print(url)
        except:
            pass
    
    def run(self):
        pool = ThreadPoolExecutor(max_workers=10)
        with open(self.wordlist, 'r') as f:
            while True:
                try:
                    line = f.readline()
                    if len(line) == 0:
                        break
                    if line.startswith('#'):
                        continue
                    
                    url = self.url + line.strip()
                    pool.submit(self.req_generator, url)
                except KeyboardInterrupt:
                    print("\n\nExiting the program now!")
                    sys.exit()
        
        pool.shutdown()

if __name__ == '__main__':
    finder = DirectoryEnumerate()
    finder.run()
                    


