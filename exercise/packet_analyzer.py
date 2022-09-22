import struct
import socket
import binascii
import sys

s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
print("""
             **************Packet Analyzer*******************
""")

while True:
    try:
        pkt = s.recvfrom(2048)

        print('------------------Ethernet Header Information---------------------')
        ether_header = pkt[0][0:14]
        eth_hdr = struct.unpack('!6s6s2s', ether_header)
        destination_mac = binascii.hexlify(eth_hdr[0]).decode('utf-8')
        source_mac = binascii.hexlify(eth_hdr[1]).decode('utf-8')
        print('Destination MAC Address: %s' % destination_mac)
        print('Source MAC address: %s\n\n' % source_mac)

        print('---------------------IP Header Information------------------------')
        ip_header = pkt[0][14:34]
        ip_hdr = struct.unpack('!12s4s4s', ip_header)
        source_ip = socket.inet_ntoa(ip_hdr[1])
        destination_ip = socket.inet_ntoa(ip_hdr[2])
        print('Destination IP Address: %s' % destination_ip)
        print('Source IP Address: %s\n\n' % source_ip)

        print('------------------TCP Header Information---------------------')
        tcp_header = pkt[0][34:54]
        tcp_hdr = struct.unpack('!HH9ss6s', tcp_header)
        source_port = tcp_hdr[0]
        destination_port = tcp_hdr[1]
        print('Destination Port: %d' % destination_port)
        print('Source Port: %d' % source_port)

    except KeyboardInterrupt:
        print('Exit the program now!')
        sys.exit()