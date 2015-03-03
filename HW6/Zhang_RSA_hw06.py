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

    e = 65537

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


def encryption(inputfile, outputfile, public_key):

    fout = open(outputfile, 'w')

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

    for C_text in cipherText:
        fout.write(C_text)

    fout.close()


def decryption(inputfile, outputfile, private_key, p, q):

    fout = open(outputfile, 'w')

    bv = BitVector(filename=inputfile)
    plainText = []

    d = private_key[0]
    n = private_key[1]

    p_bv = BitVector(intVal=p)
    q_bv = BitVector(intVal=q)

    p_MI_bv = p_bv.multiplicative_inverse(q_bv)
    q_MI_bv = q_bv.multiplicative_inverse(p_bv)

    p_MI = int(p_MI_bv)
    q_MI = int(q_MI_bv)

    while bv.more_to_read:

        bitvector = bv.read_bits_from_file(256)

        C = int(bitvector)

        Vp = pow(C, d, p)
        Vq = pow(C, d, q)

        Xp = q * q_MI
        Xq = p * p_MI

        M = (Vp * Xp + Vq * Xq) % n
        M_bv = BitVector(intVal=M, size=128)
        M_text = M_bv.get_text_from_bitvector()
        plainText.append(M_text)

    for M_text in plainText:
        fout.write(M_text)

    fout.close()



if __name__ == "__main__":
    '''
    arg1 = 20
    arg2 = 49
    gcdval = bgcd(arg1, arg2)
    print("BGCD is: ", gcdval)

    '''

    if len(sys.argv) != 4:
        exit()

    plainTextFile = sys.argv[1]
    encryptedfile = sys.argv[2]
    decryptedfile = sys.argv[3]


    keyList = getKey()

    public_key = keyList[0]
    private_key = keyList[1]
    p = keyList[2]
    q = keyList[3]

    encryption(plainTextFile, encryptedfile, public_key)
    decryption(encryptedfile, decryptedfile, private_key, p , q)

    '''
    if sys.argv[1] == "-e":
        encryption(inputfile, outputfile, public_key)
    elif sys.argv[2] == "-d":
        decryption()
    else:
        exit()
    '''