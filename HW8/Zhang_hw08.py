#! /usr/bin/env python

__author__ = 'Jinyi Zhang'

import socket

class TcpAttack:

    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarget(self, rangeStart, rangeEnd):

        f = open("openports.txt", 'w')
        f.write("Opened ports: \n")

        for port in range(rangeStart, rangeEnd):

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.settimeout(0.5)

            result = s.connect_ex((self.targetIP, port))

            if (result == 0):
                # connect succeed, so port is open
                #print("Open Port: {0}". format(port))
                f.write("Port: {}\n".format(port))

            s.close()

        f.close()

    def attackTarget(self, port):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(5)

        

if __name__ == "__main__":

    tcp = TcpAttack('localhost', 'sopa.ecn.purdue.edu')

    tcp.scanTarget(20, 445)