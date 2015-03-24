#! /usr/bin/env python

__author__ = 'Jinyi Zhang'

from socket import *
import subprocess
import sys


class TcpAttack:

    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarget(self, rangeStart, rangeEnd):
        pass


    def attackTarget(self, port):
        pass

if __name__ == "__main__":

    pass