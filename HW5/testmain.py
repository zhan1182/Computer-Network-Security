#! /usr/bin/env python

__author__ = 'zhan1182'


from hw05 import *

if __name__ == "__main__":
    rc4cipher = RC4('lukeimyourfather')
    originalImage = rc4cipher.getbody("Tiger2.ppm")

    encryptedImage = rc4cipher.encrypt(originalImage)
    decryptedImage = rc4cipher.decrypt(encryptedImage)

    if originalImage == decryptedImage:
        print("Awesome")
    else:
        print("Fishy")