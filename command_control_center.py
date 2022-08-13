from unicodedata import name
import paramiko
import sys

class MySSHClient:
    def __init__(self,host,port,username,password) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            print('%s %d %s %s ' % (self.host, self.port, self.username, self.password))
            self.sshclient.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
            print('[-] Connected successfully to %s' % self.host)
        except Exception as e:
            print('[-] Failed to connect to %s: %s' % (self.host, e))
    
    def execute_command(self,command):
        try:
            stdin, stdout,stderr = self.sshclient.exec_command(command)
            if stdout:
                return stdout.read().decode('utf-8')
            if stderr:
                return "Failed to execute command on %s" % self.host

        except:
            return "Failed to execute command %s" % self.host
    

    
    
class CommandAndControlCenter:
    def __init__(self) -> None:
        banner = """
        **********************************************************************
        **********************************************************************
        **********************Command and Control Center by Jason-huawen******
        **********************************************************************
        **********************************************************************

        """
        print(banner)
        
        self.client_list = []
    
    def menu(self):
        menu = """
        
                    1       Add client
                    2       List client
                    3       Execute Command
                    4       Quit
        """
        print(menu)

    def add_client(self):
        host = input("Target IP address: ")
        port = input('Port(Default 22): ')
        if port == '':
            port = 22
        username = input("Username: ")
        password = input("Password: ")
        client = MySSHClient(host, int(port),username, password)
        self.client_list.append(client)

    def list_clients(self):
        print("Clients as follows:\n")
        for client in self.client_list:
            print('\t',client.host)

    def run_all_command(self):
        while True:
            command = input('Command to send: ')
            if command == 'exit':
                break
            for client in self.client_list:
                result = client.execute_command(command)
                print('Execute result from %s: \n%s' % (client.host, result))

    def run(self):
        while True:
            self.menu()
            option = input("Please select options: ")
            if option == '1':
                self.add_client()
            elif option == '2':
                self.list_clients()
            elif option == '3':
                self.run_all_command()
            elif option == '4':
                break
            else:
                print('Wrong option, input again!!!')

                
if __name__ == '__main__':
    center = CommandAndControlCenter()
    center.run()
