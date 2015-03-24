#! /usr/bin/env python

__author__ = 'Jinyi'

import socket

def scanTarget(rangeStart, rangeEnd):

    HOST = 'sopa.ecn.purdue.edu'

    for port in range(rangeStart, rangeEnd):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(0.1)

        result = s.connect_ex((HOST, port))

        if (result == 0):
            # connect succeed, so port is open
            print("Open Port: {0}". format(port))
        else:
            print("Port closed: {0}".format(port))

        s.close()

if __name__ == "__main__":
    scanTarget(20, 1025)


