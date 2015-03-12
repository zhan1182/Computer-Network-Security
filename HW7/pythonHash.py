#! /usr/bin/env python

__author__ = 'zhan1182'

import hashlib


if __name__ == "__main__":


    filename = "message.txt"

    fin = open(filename, 'r')

    message = fin.read().strip("\n")

    #MD_sha512 = hashlib.sha512(message)
    MD_sha1 = hashlib.sha1(message)

    #print(MD_sha512.hexdigest())
    print(MD_sha1.hexdigest())

    fin.close()




