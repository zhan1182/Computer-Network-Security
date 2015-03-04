#! /usr/bin/env python

__author__ = "Jinyi Zhang"

from BitVector import *
from PrimeGenerator import *
import numpy as np
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

# Get the key list using the e as 3, which includes d, n, p and q.
def getKey():

    # Using a small e value in order to do the crack
    e = 3

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

    # Build the public key
    public_key = [e, n]

    return public_key


def encryption(inputfile, public_key):

    bv = BitVector(filename = inputfile)

    cipherText = []

    # Read the bits from the inputfile
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)

        while(bitvec.length() < 128):
            bitvec = bitvec + BitVector(textstring="\n")

        # append newline characters until the length reach 128
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
        print(C_HEX)

        # Output the bits in text format
        cipherText.append(C_text)

    #print(cipherText)

    return cipherText

# Get the cube root of the given integer.
# Download from ECE404 website
def solve_pRoot(p,y):
    p = long(p);
    y = long(y);
    # Initial guess for xk
    try:
        xk = long(pow(y,1.0/p));
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y;
        a = 0;
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1;
            a += 1;
        # log xk = log2 y / p
        # log xk = (a + log2 y0) / p
        xk = long(pow(2.0, ( a + np.log2(float(y0)) )/ p ));
    # Solve for x using Newton's Method
    err_k = pow(xk,p)-y;
    while (abs(err_k) > 1):
        gk = p*pow(xk,p-1);
        err_k = pow(xk,p)-y;
        xk = -err_k/gk + xk;
    return xk


# Implement the crack, using CRT algorithm
# Assuming e = 3
def crack(key1, key2, key3, C1, C2, C3, crackfile):

    fout = open(crackfile, 'w')

    # Get the three different n values
    n1 = key1[1]
    n2 = key2[1]
    n3 = key3[1]

    # Build the modulus
    N = n1 * n2 * n3

    N1 = N / n1
    N2 = N / n2
    N3 = N / n3

    # Calculate the MI of each Ni
    bv_N1 = BitVector(intVal=N1)
    bv_N2 = BitVector(intVal=N2)
    bv_N3 = BitVector(intVal=N3)

    bv_n1 = BitVector(intVal=n1)
    bv_n2 = BitVector(intVal=n2)
    bv_n3 = BitVector(intVal=n3)

    MI_bv_N1 = bv_N1.multiplicative_inverse(bv_n1)
    MI_bv_N2 = bv_N2.multiplicative_inverse(bv_n2)
    MI_bv_N3 = bv_N3.multiplicative_inverse(bv_n3)

    MI_N1 = int(MI_bv_N1)
    MI_N2 = int(MI_bv_N2)
    MI_N3 = int(MI_bv_N3)

    M_List = []

    # Do the crack
    for ct in range(len(C1)):

        # Get the ai
        a1_bv = BitVector(textstring=C1[ct])
        a1 = int(a1_bv)
        a2_bv = BitVector(textstring=C2[ct])
        a2 = int(a2_bv)
        a3_bv = BitVector(textstring=C3[ct])
        a3 = int(a3_bv)

        # Build the cube of M, since e = 3
        M_cube = (a1 * N1 * MI_N1 + a2 * N2 * MI_N2 + a3 * N3 * MI_N3) % N

        # Take the cube root
        M = solve_pRoot(3, M_cube)

        # Construct the plaintext list
        M_bv = BitVector(intVal=M, size=128)
        M_List.append(M_bv.get_text_from_bitvector())

        print(M_bv.get_hex_string_from_bitvector())

    # Output the cracked text
    for M in M_List:
        fout.write(M)

    fout.close()





if __name__ == "__main__":

    if len(sys.argv) != 3:
        exit()

    # Get the input and output filenames
    plainTextFile = sys.argv[1]
    crakedFile = sys.argv[2]

    # Generate three different public key using e = 3
    public_key1 = getKey()
    public_key2 = getKey()
    public_key3 = getKey()

    print(public_key1[1])
    print(public_key2[1])
    print(public_key3[1])


    # Do the encryption three times
    C1 = encryption(plainTextFile, public_key1)
    print("--------------------------------")
    C2 = encryption(plainTextFile, public_key2)
    print("--------------------------------")
    C3 = encryption(plainTextFile, public_key3)
    print("--------------------------------")


    # Crack the encrypted text
    crack(public_key1, public_key2, public_key3, C1, C2, C3, crakedFile)