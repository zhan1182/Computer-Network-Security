#! /usr/bin/env python

__author__ = "Jinyi Zhang"

from BitVector import *
from PrimeGenerator import *
import sys


def bgcd(a,b):
    if a == b:
        return a
    if a == 0:
        return b
    if b == 0:
        return a

    if (~a & 1):
        if(b&1):
            return bgcd(a>>1, b)
        else:
            return bgcd(a >> 1, b >> 1) << 1
    if(~b & 1):
        return bgcd(a, b >> 1)
    if(a > b):
        return bgcd((a - b) >> 1, b)

    return bgcd((b - a) >> 1, a)


def getKey():

    e = 3

    while 1:
        generator = PrimeGenerator(bits = 128, debug = 0)
        p = generator.findPrime()
        q = generator.findPrime()

        p_bv = BitVector(intVal=p, size=128)
        q_bv = BitVector(intVal=q, size=128)

        if p != q:
            if p_bv[0] & p_bv[1] & q_bv[0] & q_bv[1] == 1:
                if bgcd((p - 1), e) == 1 and bgcd((q- 1), e) == 1:
                    break

    n = p * q
    n_totient = (p - 1) * (q - 1)
    n_totient_bv = BitVector(intVal = n_totient)
    e_bv = BitVector(intVal = e)
    d_bv = e_bv.multiplicative_inverse(n_totient_bv)
    d = int(d_bv)

    public_key = [e, n]
    private_key = [d, n]

    KeyList = public_key, private_key, p, q

    #print(KeyList)

    return KeyList


def encryption(inputfile, public_key):

    bv = BitVector(filename = inputfile)

    cipherText = []

    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)

        while(bitvec.length() < 128):
            bitvec = bitvec + BitVector(textstring="\n")

        bitvec.pad_from_left(128)

        M = int(bitvec)

        e = public_key[0]
        n = public_key[1]
        C = pow(M, e, n)

        C_bv = BitVector(intVal=C, size=256)
        C_text = C_bv.get_text_from_bitvector()

        cipherText.append(C_text)

    return cipherText


if __name__ == "__main__":

    if len(sys.argv) != 3:
        exit()

    plainTextFile = sys.argv[1]
    crakedFile = sys.argv[2]

    keyList1 = getKey()
    keyList2 = getKey()
    KeyList3 = getKey()

    public_key1 = keyList1[0]
    public_key2 = keyList2[0]
    public_key3 = keyList3[0]

    C1 = encryption(plainTextFile, public_key1)
    C2 = encryption(plainTextFile, public_key2)
    C3 = encryption(plainTextFile, public_key3)

    