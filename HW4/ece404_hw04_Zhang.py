#!/usr/bin/env python

__author__ = 'Jinyi Zhang'

import sys
from BitVector import *
import copy

def getSbox(choice):
    AES_modulus = BitVector(bitstring='100011011')
    subBytesTable = []                                                  # for encryption
    invSubBytesTable = []                                               # for decryption
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For byte scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For byte scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))
    if choice == "encrypt" or choice == "KeySbox":
        return subBytesTable
    elif choice == "decrypt":
        return invSubBytesTable

# Do the byte to byte substitution
def getSubByte(bitvec, Sbox):
    [LE, RE] = bitvec.divide_into_two()

    row = int(LE)
    col = int(RE)

    retint = Sbox[row * 16 + col]
    #print(retint)

    retbv = BitVector(intVal=retint, size=8)

    return retbv

# Generate the Round Constant
def getRoundConstant():

    AES_modulus = BitVector(bitstring='100011011')

    RC = BitVector(intVal=1, size=8)
    MUL = BitVector(intVal=2, size=8)

    BVlist = []
    for ct in range(0,10):
        BVlist.append(RC)
        RC = RC.gf_multiply_modular(MUL, AES_modulus, 8)

    print("length = {}".format(len(BVlist)))

    for bvconstant in BVlist:
        print(bvconstant.get_hex_string_from_bitvector())

    return BVlist

# Definition for the G function
def gfunction(bvword, Sbox, RC4Bytes):

    # step 1, left shift 1 byte
    bvword_copy = copy.copy(bvword)
    bvword_copy = bvword_copy << 8
    #print(bvword_copy.get_hex_string_from_bitvector())

    # step 2, byte-substitution
    [LE, RE] = bvword_copy.divide_into_two()
    [firstByte, secondByte] = LE.divide_into_two()
    [thirdByte, fourthByte] = RE.divide_into_two()
    RetBv = BitVector(size=0)
    RetBv += getSubByte(firstByte, Sbox) + getSubByte(secondByte, Sbox) + getSubByte(thirdByte, Sbox) + getSubByte(fourthByte, Sbox)
    #print(RetBv.get_hex_string_from_bitvector())

    # step 3, XOR round constant
    RetBv[0:8] = RetBv[0:8] ^ RC4Bytes
    #print(RetBv.get_hex_string_from_bitvector())
    return RetBv

# Generate the key schedule
def getkeyschedule(mykey, Sbox):

    # get the round constant list
    RClist = getRoundConstant()
    #print(len(RClist))

    # assume mykey is a 16 bytes string, which is 4 words
    # key schedule is a list, which contains 44 bit vectors. Each bit vector is a word.
    # Generate first 4 bytes
    keyschedule = []
    for ct in range(4):
        ind = 4 * ct
        word = BitVector(textstring=(mykey[ind] + mykey[ind+1] + mykey[ind+2] + mykey[ind+3]))
        keyschedule.append(word)

    #for word in keyschedule:
    #    print(word.get_hex_string_from_bitvector())

    # Expand the key
    for ct in range(4,44):
        if ct % 4 == 0:
            word = keyschedule[ct-4] ^ (gfunction(keyschedule[ct - 1], Sbox, RClist[ct / 4 - 1]))
        else:
            word = keyschedule[ct-1] ^ keyschedule[ct-4]
        keyschedule.append(word)

    #for word in keyschedule:
    #    print(word.get_hex_string_from_bitvector())
    return keyschedule

# Shift Rows
def shiftRow(bitvec):
    # Generate the Rows
    row1 = bitvec[0:8] + bitvec[32:40] + bitvec[64:72] + bitvec[96:104]
    row2 = bitvec[8:16] + bitvec[40:48] + bitvec[72:80] + bitvec[104:112]
    row3 = bitvec[16:24] + bitvec[48:56] + bitvec[80:88] + bitvec[112:120]
    row4 = bitvec[24:32] + bitvec[56:64] + bitvec[88:96] + bitvec[120:128]

    # Shift the Rows
    row2 = row2 << 8
    row3 = row3 << 16
    row4 = row4 << 24

    # Make shifted state array
    retBV = BitVector(size=0)

    for ct in range(4):
        retBV += row1[(ct*8):(ct*8)+8] + row2[(ct*8):(ct*8)+8] + row3[(ct*8):(ct*8)+8] + row4[(ct*8):(ct*8)+8]

    return retBV

# Inverse shift rows
def InvShiftRow(bitvec):
    # Generate the rows
    row1 = bitvec[0:8] + bitvec[32:40] + bitvec[64:72] + bitvec[96:104]
    row2 = bitvec[8:16] + bitvec[40:48] + bitvec[72:80] + bitvec[104:112]
    row3 = bitvec[16:24] + bitvec[48:56] + bitvec[80:88] + bitvec[112:120]
    row4 = bitvec[24:32] + bitvec[56:64] + bitvec[88:96] + bitvec[120:128]

    # Shift the Rows
    row2 = row2 >> 8
    row3 = row3 >> 16
    row4 = row4 >> 24

    # Make the shifted state array
    retBV = BitVector(size=0)

    for ct in range(4):
        retBV += row1[(ct*8):(ct*8)+8] + row2[(ct*8):(ct*8)+8] + row3[(ct*8):(ct*8)+8] + row4[(ct*8):(ct*8)+8]

    return retBV

# Mix column
def mixCol(bitvec):
    AES_modulus = BitVector(bitstring='100011011')

    MUL02 = BitVector(intVal=2, size=8)
    MUL03 = BitVector(intVal=3, size=8)

    row1 = bitvec[0:8] + bitvec[32:40] + bitvec[64:72] + bitvec[96:104]
    row2 = bitvec[8:16] + bitvec[40:48] + bitvec[72:80] + bitvec[104:112]
    row3 = bitvec[16:24] + bitvec[48:56] + bitvec[80:88] + bitvec[112:120]
    row4 = bitvec[24:32] + bitvec[56:64] + bitvec[88:96] + bitvec[120:128]

    row5 = BitVector(intVal=0,size=32)
    row6 = BitVector(intVal=0,size=32)
    row7 = BitVector(intVal=0,size=32)
    row8 = BitVector(intVal=0,size=32)

    for ct in range(4):
        factor1 = row1[(ct*8):(ct*8)+8].gf_multiply_modular(MUL02, AES_modulus, 8)
        factor2 = row2[(ct*8):(ct*8)+8].gf_multiply_modular(MUL03, AES_modulus, 8)
        row5[(ct*8):(ct*8)+8] = factor1 ^ factor2 ^ row3[(ct*8):(ct*8)+8] ^ row4[(ct*8):(ct*8)+8]

    for ct in range(4):
        factor1 = row2[(ct*8):(ct*8)+8].gf_multiply_modular(MUL02, AES_modulus, 8)
        factor2 = row3[(ct*8):(ct*8)+8].gf_multiply_modular(MUL03, AES_modulus, 8)
        row6[(ct*8):(ct*8)+8] = row1[(ct*8):(ct*8)+8] ^ factor1 ^ factor2 ^ row4[(ct*8):(ct*8)+8]

    for ct in range(4):
        factor1 = row3[(ct*8):(ct*8)+8].gf_multiply_modular(MUL02, AES_modulus, 8)
        factor2 = row4[(ct*8):(ct*8)+8].gf_multiply_modular(MUL03, AES_modulus, 8)
        row7[(ct*8):(ct*8)+8] = row1[(ct*8):(ct*8)+8] ^ row2[(ct*8):(ct*8)+8] ^ factor1 ^ factor2

    for ct in range(4):
        factor1 = row4[(ct*8):(ct*8)+8].gf_multiply_modular(MUL02, AES_modulus, 8)
        factor2 = row1[(ct*8):(ct*8)+8].gf_multiply_modular(MUL03, AES_modulus, 8)
        row8[(ct*8):(ct*8)+8] = factor2 ^ row2[(ct*8):(ct*8)+8] ^ row3[(ct*8):(ct*8)+8] ^ factor1

    retBV = BitVector(size=0)

    for ct in range(4):
        retBV += row5[(ct*8):(ct*8)+8] + row6[(ct*8):(ct*8)+8] + row7[(ct*8):(ct*8)+8] + row8[(ct*8):(ct*8)+8]

    return retBV

# Inverse mix column
def InvMixCol(bitvec):
    AES_modulus = BitVector(bitstring='100011011')

    MUL0E = BitVector(intVal=14, size=8)
    MUL0B = BitVector(intVal=11, size=8)
    MUL0D = BitVector(intVal=13, size=8)
    MUL09 = BitVector(intVal=9, size=8)

    row1 = bitvec[0:8] + bitvec[32:40] + bitvec[64:72] + bitvec[96:104]
    row2 = bitvec[8:16] + bitvec[40:48] + bitvec[72:80] + bitvec[104:112]
    row3 = bitvec[16:24] + bitvec[48:56] + bitvec[80:88] + bitvec[112:120]
    row4 = bitvec[24:32] + bitvec[56:64] + bitvec[88:96] + bitvec[120:128]

    row5 = BitVector(intVal=0,size=32)
    row6 = BitVector(intVal=0,size=32)
    row7 = BitVector(intVal=0,size=32)
    row8 = BitVector(intVal=0,size=32)

    for ct in range(4):
        factor1 = row1[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0E, AES_modulus, 8)
        factor2 = row2[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0B, AES_modulus, 8)
        factor3 = row3[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0D, AES_modulus, 8)
        factor4 = row4[(ct*8):(ct*8)+8].gf_multiply_modular(MUL09, AES_modulus, 8)

        row5[(ct*8):(ct*8)+8] = factor1 ^ factor2 ^ factor3 ^ factor4

    for ct in range(4):
        factor1 = row1[(ct*8):(ct*8)+8].gf_multiply_modular(MUL09, AES_modulus, 8)
        factor2 = row2[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0E, AES_modulus, 8)
        factor3 = row3[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0B, AES_modulus, 8)
        factor4 = row4[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0D, AES_modulus, 8)

        row6[(ct*8):(ct*8)+8] = factor1 ^ factor2 ^ factor3 ^ factor4

    for ct in range(4):
        factor1 = row1[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0D, AES_modulus, 8)
        factor2 = row2[(ct*8):(ct*8)+8].gf_multiply_modular(MUL09, AES_modulus, 8)
        factor3 = row3[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0E, AES_modulus, 8)
        factor4 = row4[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0B, AES_modulus, 8)

        row7[(ct*8):(ct*8)+8] = factor1 ^ factor2 ^ factor3 ^ factor4

    for ct in range(4):
        factor1 = row1[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0B, AES_modulus, 8)
        factor2 = row2[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0D, AES_modulus, 8)
        factor3 = row3[(ct*8):(ct*8)+8].gf_multiply_modular(MUL09, AES_modulus, 8)
        factor4 = row4[(ct*8):(ct*8)+8].gf_multiply_modular(MUL0E, AES_modulus, 8)

        row8[(ct*8):(ct*8)+8] = factor1 ^ factor2 ^ factor3 ^ factor4

    retBV = BitVector(size=0)

    for ct in range(4):
        retBV += row5[(ct*8):(ct*8)+8] + row6[(ct*8):(ct*8)+8] + row7[(ct*8):(ct*8)+8] + row8[(ct*8):(ct*8)+8]

    return retBV

# Begin AES algorithem
def AES(choice, mykey):
    Sbox = getSbox(choice)
    keySbox = getSbox("KeySbox")
    #print(keySbox)
    #print(Sbox)
    keyschedule = getkeyschedule(mykey, keySbox)
    if choice == "encrypt":
        #print(len(keyschedule))
        #for key in keyschedule:
        #    print(key.get_hex_string_from_bitvector())
        inputfile = "plaintext.txt"
        outputfile = "encryptedtext.txt"
        bv = BitVector(filename = inputfile )
        fout = open(outputfile,'w')
        while(bv.more_to_read):
            # Read 128 bits from the input file
            bitvec = bv.read_bits_from_file(128)

            # get rid of the last new line byte
            if bitvec.length() == 8:
                break

            # add the padding if necessary
            mod = bitvec.length() % 128
            if not mod == 0:
                bitvec.pad_from_right(128 - mod)

            # before 10 rounds, XOR the key W0 to W3
            bitvec = bitvec ^ (keyschedule[0] + keyschedule[1] + keyschedule[2] + keyschedule[3])

            # begin 10 rounds
            for i in range(1, 11):

                # Step1, SubBytes
                for ct in range(16):
                    bitvec[(ct*8):(ct*8)+8] = getSubByte(bitvec[(ct*8):(ct*8)+8], Sbox)

                # Step2, ShiftRows
                bitvec = shiftRow(bitvec)

                # Step3, if not the last round, MixColumns
                if i != 10:
                    bitvec = mixCol(bitvec)

                # Step4, Add Round key
                bitvec = bitvec ^ (keyschedule[4 * i] + keyschedule[4 * i + 1] + keyschedule[4 * i + 2] + keyschedule[4 * i + 3])

            #print(bitvec.get_hex_string_from_bitvector())
            fout.write(bitvec.get_text_from_bitvector())
            #bitvec.write_to_file(fout)

        fout.close()

    elif choice == "decrypt":
        inputfile = "encryptedtext.txt"
        outputfile = "decryptedtext.txt"
        bv = BitVector(filename = inputfile )
        fout = open(outputfile,'w')
        while(bv.more_to_read):
            # Read 128 bits from the input file
            bitvec = bv.read_bits_from_file(128)

            #print(bitvec.get_hex_string_from_bitvector())

            if bitvec.length() == 8:
                break

            # add the padding if necessary
            mod = bitvec.length() % 128
            if not mod == 0:
                bitvec.pad_from_right(128 - mod)


            # before 10 rounds, XOR the round key W40 to W43
            bitvec = bitvec ^ (keyschedule[40] + keyschedule[41] + keyschedule[42] + keyschedule[43])

            # begin 10 rounds
            for i in range(1, 11):
                # Step1, Inverse ShiftRows
                bitvec = InvShiftRow(bitvec)

                # Step2, Inverse SubBytes
                for ct in range(16):
                    bitvec[(ct*8):(ct*8)+8] = getSubByte(bitvec[(ct*8):(ct*8)+8], Sbox)

                # Step3, Add Round key
                bitvec = bitvec ^ (keyschedule[(10-i) * 4] + keyschedule[(10-i) * 4 + 1] + keyschedule[(10-i) * 4 + 2] + keyschedule[(10-i) * 4 + 3])

                # Step4, if not at last round, Inverse MixColumns
                if i != 10:
                    bitvec = InvMixCol(bitvec)

            fout.write(bitvec.get_text_from_bitvector())
            #bitvec.write_to_file(fout)

        fout.close()

# Ask User for the key
def getkey():
    ## ask user for input
    mykey = raw_input("Enter your 16 bytes key: ")
    ## make sure it satisfies any constraints on the key
    while not len(mykey) == 16 or not mykey.isalpha():
        print("Your key should be 16 English charaters.")
        mykey = raw_input("Enter your 16 bytes key: ")
    return mykey


def main():

    mykey = getkey()

    while True:
        choice = raw_input("encrypt or decrypt? ")
        if choice == "encrypt" or choice == "decrypt":
            break
        else:
            print("Please enter either encrypt or decrypt.")

    #mykey = "lukeimyourfather"
    #choice = "encrypt"
    #choice = "decrypt"
    AES(choice, mykey)



if __name__ == "__main__":
    main()
