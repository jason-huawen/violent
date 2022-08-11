import paramiko
import sys
import optparse
import getpass

class MySSHClient:
    def __init__(self) -> None:
        self.target = self.get_params()[0]
        self.port = self.get_params()[1]
        self.username = self.get_params()[2]

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -t target ip address -p port -u username' % sys.argv[0])
        parser.add_option('-t', '--target', dest='target', type='string', help='Specify target IP address to connect')
        parser.add_option('-p', '--port', dest='port', type='int', help='Specify port')
        parser.add_option('-u', '--username', dest='username', type='string', help='Specify username')
        options, args = parser.parse_args()
        if options.port is None:
            options.port = 22
        if options.target is None:
            print(parser.usage)
            print('Please specify target IP address')
            sys.exit()
        if options.username is None:
            print(parser.usage)
            print('Please specify username')
            sys.exit()
        return options.target, options.port, options.username
    
    def run(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        password = getpass.getpass('Please input password: ')
        try:
            ssh_client.connect(hostname=self.target,port=self.port,username=self.username, password=password)
        except Exception as e:
            print('Failed to authenticate',e)
            sys.exit()
        try:
            while True:
                command = input('[%s]$ ' % self.target)
                if command == 'exit':
                    break
                stdin, stdout, stderr = ssh_client.exec_command(command)
                if stdout:
                    print(stdout.read().decode('utf-8').strip())
                if stderr:
                    print(stderr.read().decode('utf-8').strip())
        except KeyboardInterrupt:
            print('Exiting the program now')
            sys.exit()
        except Exception as e:
            print('Error happened: %s' % e)
    

if __name__ == '__main__':
    client = MySSHClient()
    client.run()