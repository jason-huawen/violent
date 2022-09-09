import socket
import os
import subprocess

def display_machine_info():
    hostname = socket.gethostname()
    host_ip_addr = socket.gethostbyname(hostname)
    os_type = os.name
    os_version_info = None
    if os_type == 'posix':
        os_version_info = subprocess.check_output(['uname', '-a']).decode('utf-8')
    print('The information about this machine:\n')
    print('Hostname: %s' % hostname)
    print('IP address: %s' % host_ip_addr)
    print('OS type: %s' % os_type)
    if os_version_info:
        print("OS version info: %s" % os_version_info)

if __name__ == '__main__':
    display_machine_info()
    