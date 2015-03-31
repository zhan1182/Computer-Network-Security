#! /usr/bin/env python

__author__ = 'zhan1182'

from BitVector import *
import copy

class RC4:

    def __init__(self, key):
        # get the key
        self.key = key

        # initialize the T vector
        self.T_Vector = []

        # initialize the StateVector
        self.SV = range(256)

        # build the T vector
        for i in range(256):
            key_bv = BitVector(textstring = self.key[i % 16])
            self.T_Vector.append(int(key_bv))

        # build the StateVector for using
        j = 0
        for i in range(256):
            j = (j + self.SV[i] + self.T_Vector[j]) % 256
            self.SV[i], self.SV[j] = self.SV[j], self.SV[i]

    # get the body of the image. The input is the filename of the image
    def getbody(self, image):
        fin = open(image, 'r')
        body = []

        self.lines = fin.readlines()

        # Build the body as a list
        for i in range(5, len(self.lines)):
            for j in range(len(self.lines[i])):
                body.append(ord(self.lines[i][j]))

        fin.close()

        return body

    # Do the encryption to the body of the image
    def encrypt(self, body):

        #print(self.SV)

        # Copy the StateVector, so that it won't be changed after using
        SV_encrypt = copy.copy(self.SV)

        # create an output image, and write header information to it
        fout = open("encrypted.ppm", 'wba')

        for i in range(5):
            fout.write(self.lines[i])

        # Do the encryption to the body of the image
        ct = 0
        output_encrypted = []

        bodylen = len(body)

        i = 0
        j = 0
        while 1:
            i = (i + 1) % 256
            j = (j + SV_encrypt[i]) % 256
            tmp = SV_encrypt[i]
            SV_encrypt[i] = SV_encrypt[j]
            SV_encrypt[j] = tmp
            k = (SV_encrypt[i] + SV_encrypt[j]) % 256
            output_encrypted.append(SV_encrypt[k] ^ body[ct])
            ct += 1
            if ct == bodylen:
                break

        # Write the body information to the output image
        fout.write(bytearray(output_encrypted))

        fout.close()

        # return the encrypted body information
        return output_encrypted

    # Do the decryption to the body of the image
    def decrypt(self, body):

        #print(self.SV)

        # Copy the StateVector, so that it won't be changed after using
        SV_decrypted = copy.copy(self.SV)

        # create an output image, and write header information to it
        fout = open("decrypted.ppm", "wba")

        for i in range(5):
            fout.write(self.lines[i])

        # Do the decryption to the body of the image
        ct = 0
        output_decrypted = []

        bodylen = len(body)

        i = 0
        j = 0
        while 1:
            i = (i + 1) % 256
            j = (j + SV_decrypted[i]) % 256
            tmp = SV_decrypted[i]
            SV_decrypted[i] = SV_decrypted[j]
            SV_decrypted[j] = tmp
            k = (SV_decrypted[i] + SV_decrypted[j]) % 256
            output_decrypted.append(SV_decrypted[k] ^ body[ct])
            ct += 1
            if ct == bodylen:
                break

        # Write the body information to the output image
        fout.write(bytearray(output_decrypted))

        fout.close()

        # return the decrypted body information
        return output_decrypted


if __name__ == "__main__":
    rc4cipher = RC4('lukeimyourfather')
    originalImage = rc4cipher.getbody("Tiger2.ppm")

    encryptedImage = rc4cipher.encrypt(originalImage)
    decryptedImage = rc4cipher.decrypt(encryptedImage)

    if originalImage == decryptedImage:
        print("Awesome")
    else:
        print("Fishy")