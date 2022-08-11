import nmap
import sys
import termcolor

class ScannerWithNmap:
    def __init__(self) -> None:
        self.banner()


    def banner(self):
        banner = """
        *****************************************************************************
        *****************************************************************************
        ****************************%s****************
        *****************************************************************************
        *****************************************************************************

        """ % termcolor.colored("Port Scanner by Jason-Huawen v1.0",'blue')
        print(banner)

    def scan_options(self):
        options = """
            1 SYN Scan
            2 Service Scan
            3 OS Scan\n
        """
        print(options)
    
    def scan_nmap(self, target, ports, options):
        scanner = nmap.PortScanner()
        try:
            result = scanner.scan(hosts=target, ports=ports,arguments=options)['scan']
            hosts = scanner.all_hosts()
            for host in hosts:
                host_status = result[host]['status']['state']
                print("%s status: %s" % (host, host_status))
                ports_status = result[host]['tcp']
                print("\tPort\tState\tName\tProduct\tVersion")
                for port,port_info in ports_status.items():
                    port_state = port_info['state']
                  
                    if port_info.get('name'):
                        name = port_info['name']
                        # print(name)
                    else:
                        name = "None"
                    if port_info.get('product'):
                        product = port_info['product']
                        # print(product)
                    else:
                        product = "None"
                    if port_info.get('version'):
                        version = port_info['version']
                        # print(version)
                    else:
                        version = "None"
                    print("\t%d\t%s\t%s\t%s\t%s"%(port, port_state,name, product, version))
                if result[host].get('osmatch'):
                    print("OS Detection result:\n")
                    osmatch_result = result[host].get('osmatch')
                    for each in osmatch_result:
                        os_name = each['name']
                        accuracy = each['accuracy']
                        print(' %s  %s' % (os_name, accuracy))

        except Exception as e:
            print('Failed to scan: %s' % e)
            sys.exit()
        

    def run(self):
        target = input('\nPlease input your target: ')
        ports = input('\nPlease input ports or port range: ')
        self.scan_options()
        scan_option = input('\nPlease select option to scan: ')
        if scan_option == '1':
            self.scan_nmap(target,ports,'-sS')
        elif scan_option == '2':
            self.scan_nmap(target,ports,'-sV')
        elif scan_option == '3':
            self.scan_nmap(target,ports,'-O')
        else:
            print('You input invalid option')
            sys.exit()

if __name__ == '__main__':
    scanner = ScannerWithNmap()
    scanner.run()