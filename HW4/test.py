#!/usr/bin/env/python
import sys
from BitVector import *

def createLookupTable(EncryptorDecrypt):
    # Initialize 16x16 Hex Table
    LookupTable = [BitVector(intVal = x, size = 8) for x in range(256)]
    # Initialize Modulus Polynomial in GF(2^8)
    modulus = BitVector(bitstring='100011011')
    n = 8
    # Encrpyt or Decrypt
    if(EncryptorDecrypt == 'encrypt'):
        # Take the multiplicative inverse of each element in the table
        LookupTable = [LookupTable[x].gf_MI(modulus, n) for x in range(256)]
        LookupTable[0] = BitVector(intVal = 0, size = 8)
        # Do bit scrambling with special byte c
        c = BitVector(bitstring='01100011')
        # Initialize an empty 16x16 Hex Table so changed bits don't affect the calculations
        SBox = [BitVector(intVal = x, size = 8) for x in range(256)]
        for byte in range(0,256):
            for i in range(0,8):
                SBox[byte][i] = LookupTable[byte][i] ^ LookupTable[byte][(i + 4) % 8] ^ LookupTable[byte][(i + 5) % 8] ^ LookupTable[byte][(i + 6) % 8] ^ LookupTable[byte][(i + 7) % 8] ^ c[i]
    if(EncryptorDecrypt == 'decrypt'):
        # Do bit scrambling with special byte d
        d = BitVector(bitstring='00000101')
        # Initialize an empty 16x16 Hex Table so changed bits don't affect the calculations
        SBox = [BitVector(intVal = x, size = 8) for x in range(256)]
        for byte in range(0,256):
            for i in range(0,8):
                SBox[byte][i] = LookupTable[byte][i] ^ LookupTable[byte][(i + 2) % 8] ^ LookupTable[byte][(i + 5) % 8] ^ LookupTable[byte][(i + 7) % 8] ^ d[i]
                # Take the multiplicative inverse of each element in the table
        SBox = [SBox[x].gf_MI(modulus, n) for x in range(256)]
    return SBox


def subBytes(LookupTable, stateArray):
    # Substitute bytes
    subbedArray = [LookupTable[stateArray[x][0:4].int_val()*10 + stateArray[x][4:8].int_val()] for x in range(16)]
    return subbedArray


def shiftRows(stateArray, encryptdecrypt):
    # split up each row in to its own array
    rows = [stateArray[x::4] for x in range(0,4)]
    # shift each row according to the AES algorithm
    if(encryptdecrypt == 'encrypt'):
        for i in range(1,4):
            rows[i] = rows[i][i:] + rows[i][:i]
    elif(encryptdecrypt == 'decrypt'):
        for i in range(1,4):
            rows[i] = rows[i][-i:] + rows[i][:-i]
            # append the elements of the row back together in the correct order
    array = []
    for i in range(4):
        for j in range(4):
            array.append(rows[j][i])
    return array



def mixColumns(stateArray, encryptdecrypt):
    # define AES modulus
    modulus = BitVector(bitstring='100011011')
    n = 8
    # split up state array in to columns
    stateArray = [stateArray[4*x:4*x+4] for x in range(4)]
    # initialize bitvectors for mixing
    mixedArray = [BitVector(intVal = 0, size = 8) for x in range(16)]
    two = BitVector(intVal = 2, size = 8)
    three = BitVector(intVal = 3, size = 8)
    E = BitVector(intVal = 14, size = 8)
    B = BitVector(intVal = 11, size = 8)
    D = BitVector(intVal = 13, size = 8)
    nine = BitVector(intVal = 9, size = 8)
    for column in range(4):
        for row in range(4):
            #mix columns depending on which column and depending if its encrypt or decrypt
            if(encryptdecrypt == 'encrypt'):
                if(row == 0):
                    mixedArray[column*4+row] = stateArray[column][0].gf_multiply_modular(two, modulus, n) ^ stateArray[column][1].gf_multiply_modular(three, modulus, n) ^ stateArray[column][2] ^ stateArray[column][3]
                elif(row == 1):
                    mixedArray[column*4+row] = stateArray[column][0] ^ stateArray[column][1].gf_multiply_modular(two, modulus, n) ^ stateArray[column][2].gf_multiply_modular(three, modulus, n) ^ stateArray[column][3]
                elif(row == 2):
                    mixedArray[column*4+row] = stateArray[column][0] ^ stateArray[column][1] ^ stateArray[column][2].gf_multiply_modular(two, modulus, n) ^ stateArray[column][3].gf_multiply_modular(three, modulus, n)
                elif(row == 3):
                    mixedArray[column*4+row] = stateArray[column][0].gf_multiply_modular(three, modulus, n) ^ stateArray[column][1] ^ stateArray[column][2] ^ stateArray[column][3].gf_multiply_modular(two, modulus, n)
            if(encryptdecrypt == 'decrypt'):
                if(row == 0):
                    mixedArray[column+row] = stateArray[column][0].gf_multiply_modular(E, modulus, n) ^ stateArray[column][1].gf_multiply_modular(B, modulus, n) ^ stateArray[column][2].gf_multiply_modular(D, modulus, n) ^ stateArray[column][3].gf_multiply_modular(nine, modulus, n)
                elif(row == 1):
                    mixedArray[column+row] = stateArray[column][0].gf_multiply_modular(nine, modulus, n) ^ stateArray[column][1].gf_multiply_modular(E, modulus, n) ^ stateArray[column][2].gf_multiply_modular(B, modulus, n) ^ stateArray[column][3].gf_multiply_modular(D, modulus, n)
                elif(row == 2):
                    mixedArray[column+row] = stateArray[column][0].gf_multiply_modular(D, modulus, n) ^ stateArray[column][1].gf_multiply_modular(nine, modulus, n) ^ stateArray[column][2].gf_multiply_modular(E, modulus, n) ^ stateArray[column][3].gf_multiply_modular(B, modulus, n)
                elif(row == 3):
                    mixedArray[column+row] = stateArray[column][0].gf_multiply_modular(B, modulus, n) ^ stateArray[column][1].gf_multiply_modular(D, modulus, n) ^ stateArray[column][2].gf_multiply_modular(nine, modulus, n) ^ stateArray[column][3].gf_multiply_modular(E, modulus, n)
    return mixedArray


def keyExpand(key, LookupTable):
    # Generate round constant bytes
    bufferBits = BitVector(intVal = 0, size = 24)
    two = BitVector(intVal = 2, size = 8)
    roundConstant = [0] * 10
    roundConstant[0] = BitVector(intVal = 1, size = 8)
    modulus = BitVector(bitstring='100011011')
    n = 8
    for i in range(1,10):
        roundConstant[i] = roundConstant[i-1].gf_multiply_modular(two, modulus, n)
    for i in range(10):
        roundConstant[i] += bufferBits
        #print roundConstant[i]

    # Expanded Key
    expandedKey = []
    # Initialize the first four words in to a list
    words = [key[4*x:4*x+4] for x in range(4)]
    keywords = [BitVector(size = 0) for x in range(4)]
    for j in range(4):
        for i in range(4):
            keywords[j] = keywords[j] + words[j][i]

    expandedKey.append(keywords)
    # Generate the 40 other words from the first 4 words
    for i in range(10):
        newWords = [0]*4
        # Implement g() on the right word of the last 4 bit word block
        prevRightWord = expandedKey[i][3]
        # Left shift the word once to the left
        prevRightWord << 1
        # Split up the 32 bits in to 4 bytes
        byteArray = [prevRightWord[0+x*8:8+x*8] for x in range(4)]
        # Do SBox Sub
        subbedByteArray = [LookupTable[byteArray[x][0:4].int_val()*10 + byteArray[x][4:8].int_val()] for x in range(4)]
        # Return four 8 bit blocks to one 32 bit block
        prevRightWord = subbedByteArray[0] + subbedByteArray[1] + subbedByteArray[2] + subbedByteArray[3]
        # XOR word with round constant
        prevRightWord = prevRightWord ^ roundConstant[i]
        # Instantiate next 4 words
        newWords[0] = expandedKey[i][0] ^ prevRightWord
        newWords[1] = expandedKey[i][1] ^ newWords[0]
        newWords[2] = expandedKey[i][2] ^ newWords[1]
        newWords[3] = expandedKey[i][3] ^ newWords[2]
        # Append new words to our word list
        expandedKey.append(newWords)
        # Convert each word to 4 bytes
    keylist = []
    for i in range(11):
        wordlist = []
        for j in range(4):
            for k in range(4):
                wordlist.append(expandedKey[i][j][0+k*8:8+k*8])
        keylist.append(wordlist)
    return keylist



def AES(encryptdecrypt,keylist,Sbox,plaintext):
    # For encryption
    if(encryptdecrypt == 'encrypt'):
        # Add first 4 words to plaintext
        for i in range(16):
            plaintext[i] = plaintext[i] ^ keylist[0][i]
            # Start the rounds
        for i in range(10):
            # Do Sbox substitution
            subbedText = subBytes(Sbox, plaintext)
            # Shift rows
            shiftText = shiftRows(subbedText, 'encrypt')
            # Mix columns, Last round does not include mix columns step
            if(i < 9):
                mixedText = mixColumns(shiftText, 'encrypt')
            # Add round key
            for j in range(16):
                plaintext[i] = mixedText[i] ^ keylist[i+1][j]
    

    # For decryption
    if(encryptdecrypt == 'decrypt'):
        # Add first 4 words to plaintext
        for i in range(16):
            plaintext[i] = plaintext[i] ^ keylist[10]
            # Start the rounds
        for i in range(10):
            # Inverse shift rows
            shiftText = shiftRows(plaintext, 'decrypt')
            # Do Inverse Sbox substitution
            subbedText = subBytes(Sbox, shiftText)
            # Add round key
            for j in range(16):
                plaintext[i] = subbedText[i] ^ keylist[9-i][j]
                # Inverse mix columns, Last round does not include inverse mix columns step
            if(i < 9):
                plaintext = mixColumns(shiftText, 'decrypt')
        # For clarity: plaintext is called plaintext for the loop, but after the rounds it is really the cipher text
        return plaintext


def main():
    # find number of bytes in file
    input_text = open('plaintext.txt', 'r+').read()
    num_bytes = len(input_text)
    # initialize array of bitvectors for each plaintext block
    plaintextlist = (num_bytes/16 + 1) * [0]
    bv = BitVector(filename = 'plaintext.txt')
    for i in range(len(plaintextlist)-1):
        plaintextlist[i] = bv.read_bits_from_file(128)
    # file not be a multiple of 128 bits so we pad the last 128 bit block
    plaintextlist[-1] = BitVector(size = 128)
    plaintextlist[-1] = bv.read_bits_from_file(128)
    plaintextlist[-1].pad_from_right(48)
    # seperate each 128 bit block to 16 8 bit blocks
    

    for i in range(len(plaintextlist)):
        plaintextlist[i] = [plaintextlist[i][0+x*8:8+x*8] for x in range(16)]
    
    # Initilize key list in to a state array
    key = BitVector(textstring = "lukeimyourfather")
    keylist = [key[0+x*8:8+x*8] for x in range(16)]
    # Create the Sbox and Expanded key list
    Sbox = createLookupTable('encrypt')
    expandedKey = keyExpand(keylist, Sbox)
    # Perform AES encryption on each 128 bit block

    for i in range(len(plaintextlist)):
        plaintextlist[i] = AES('encrypt', expandedKey, Sbox, plaintextlist[i])
    
    # Convert cipher text into a hex string and print it in to output file
    cipherHex = ''
    for array in plaintextlist:
        for byte in array:
            cipherHex = cipherHex + byte.get_hex_string_from_bitvector()

    FILEOUT = open('encryptedtext.txt', 'wb')
    FILEOUT.write(cipherHex)
    # Initialize Sbox for decryption
    Sbox = createLookupTable('decrypt')
    # Perform AES decryption on each 128 bit block
    for i in range(len(plaintextlist)):
        plaintextlist[i] = AES('encrypt', expandedKey, Sbox, plaintextlist[i])
    # Convert decrypted text into text string and print it in to output file
    decrypted = ''
    for array in plaintextlist:
        for byte in array:
            decrypted = decrypted + byte.get_text_from_bitvector()
    FILEOUT = open('decryptedtext.txt', 'wb')
    FILEOUT.write(decrypted)
if __name__ == "__main__":
    main()
