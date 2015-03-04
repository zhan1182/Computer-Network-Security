#! /usr/bin/env python

__author__ = "Jinyi Zhang"

from BitVector import *
from PrimeGenerator import *
import sys

# Implementation of the binary GCD algorithm.
# From ECE404 Lecture 5
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

# Get the key list using the e as 65537, which includes d, n, p and q.
def getKey():

    e = 65537

    while 1:
        generator = PrimeGenerator(bits = 128, debug = 0)

        # Generate two primes for potential p and q
        p = generator.findPrime()
        q = generator.findPrime()

        # Get the bit vector for the potential p and q
        p_bv = BitVector(intVal=p, size=128)
        q_bv = BitVector(intVal=q, size=128)

        # If all conditions are satisfied, then break
        # Else, keep generating new primes and test
        if p != q:
            if p_bv[0] & p_bv[1] & q_bv[0] & q_bv[1] == 1:
                if bgcd((p - 1), e) == 1 and bgcd((q- 1), e) == 1:
                    break
    # get n
    n = p * q

    # find d via the totient of n and MI of e.
    n_totient = (p - 1) * (q - 1)
    n_totient_bv = BitVector(intVal = n_totient)

    e_bv = BitVector(intVal = e)
    d_bv = e_bv.multiplicative_inverse(n_totient_bv)
    d = int(d_bv)

    # Build the public key and private key
    public_key = [e, n]
    private_key = [d, n]


    KeyList = [public_key, private_key, p, q]

    #print(KeyList)

    return KeyList


def encryption(inputfile, outputfile, public_key):

    fout = open(outputfile, 'w')

    bv = BitVector(filename = inputfile)

    cipherText = []
    cipherHex = []

    # Read the bits from the inputfile
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)

        # append newline characters until the length reach 128
        while(bitvec.length() < 128):
            bitvec = bitvec + BitVector(textstring="\n")

        # Prepend it with 128 zeros on the left to make it a 256-bit block
        bitvec.pad_from_left(128)

        # Get the corresponding integer value
        M = int(bitvec)

        # Do the encryption
        e = public_key[0]
        n = public_key[1]
        C = pow(M, e, n)

        # Build the cipher-text list
        C_bv = BitVector(intVal=C, size=256)
        C_text = C_bv.get_text_from_bitvector()
        C_HEX = C_bv.get_hex_string_from_bitvector()

        cipherHex.append(C_HEX)
        cipherText.append(C_text)


    fhex = open("EncryptionHEX.txt", 'w')
    for C_hex in cipherHex:
        fhex.write(C_hex)
    fhex.close()


    # Output the bits in text format
    for C_text in cipherText:
        fout.write(C_text)

    fout.close()


def decryption(inputfile, outputfile, private_key, p, q):

    fout = open(outputfile, 'w')

    bv = BitVector(filename=inputfile)
    plainText = []
    plainHEX = []

    # Get the d and n of the private key
    d = private_key[0]
    n = private_key[1]

    # Calculate the MI of p and q
    p_bv = BitVector(intVal=p)
    q_bv = BitVector(intVal=q)

    p_MI_bv = p_bv.multiplicative_inverse(q_bv)
    q_MI_bv = q_bv.multiplicative_inverse(p_bv)

    p_MI = int(p_MI_bv)
    q_MI = int(q_MI_bv)

    # Read the bits from the input file
    while bv.more_to_read:

        bitvector = bv.read_bits_from_file(256)

        # Get the corresponding cipher integer C
        C = int(bitvector)

        # Do the decryption, get the integer corresponding to the plaintext M
        Vp = pow(C, d, p)
        Vq = pow(C, d, q)

        Xp = q * q_MI
        Xq = p * p_MI

        M = (Vp * Xp + Vq * Xq) % n

        # Build the plain text list
        M_bv = BitVector(intVal=M, size=128)
        M_text = M_bv.get_text_from_bitvector()

        M_HEX = M_bv.get_hex_string_from_bitvector()


        plainText.append(M_text)
        plainHEX.append(M_HEX)

    fhex = open("decryptionHEX.txt", 'w')
    for M_HEX in plainHEX:
        fhex.write(M_HEX)

    fhex.close()

    # Output the plaintext
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
    d = private_key[0]

    print(p)
    print(q)
    print(d)

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