import socket
import sys
import optparse

class SMTPUsersEnumerate:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        self.wordlist = self.get_params()[2]
        banner = """


                ____.                             __      __                      
                |    |____    __________   ____   /  \    /  \____   ____    ____  
                |    \__  \  /  ___/  _ \ /    \  \   \/\/   /  _ \ /    \  / ___\ 
            /\__|    |/ __ \_\___ (  <_> )   |  \  \        (  <_> )   |  \/ /_/  >
            \________(____  /____  >____/|___|  /   \__/\  / \____/|___|  /\___  / 
                        \/     \/           \/         \/             \//_____/  



                       SMTP Users Enumeration Tool V1.0

        """
        print(banner)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)

        try:            
            self.sock.connect((self.target, self.port))
            service_banner = self.sock.recv(1024).decode('utf-8')
            print(service_banner)            
            
        except Exception as e:
            print("Failed to connect target[%s] on port: %d" % (self.target, self.port))
            print(e)
            sys.exit()
        
       

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target -p port -w wordlist' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port of SMTP service')
        parser.add_option('-w', '--wordlist', dest='wordlist', type='string', help='Specify wordlist')
        options, args = parser.parse_args()
        if options.port is None:
            options.port = 25
        if options.target is None or options.wordlist is None:
            print(parser.usage)
            sys.exit()
        return options.target, options.port, options.wordlist



    def check_user(self,username):
        try:       
            command = "VRFY %s\n" % username
            self.sock.send(command.encode('utf-8'))
            recv_data = self.sock.recv(1024)
            if recv_data:
                data = recv_data.decode('utf-8')
                if '252' in data:
                    print('%s is valid' % username)
                elif '550' in data:
                    print('%s does not exist' % username)
                elif '503' in data:
                    print('Require authentication')
                elif '500' in data:
                    print('VRFY Command is not supported')
            
        except:
            pass
    
    def run(self):
        print('Start enumerating..')
              
        with open(self.wordlist, 'r') as f:
            for line in f.readlines():
                if len(line) > 0:
                    self.check_user(line.strip())

if __name__ == '__main__':
    enumerator = SMTPUsersEnumerate()
    enumerator.run()