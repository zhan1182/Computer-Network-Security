#!/usr/bin/env/python

### hw2_starter.py

import sys
from BitVector import *


################################   Initial setup  ################################

# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 
9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 
20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,
1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

# Initial permutation of the key (See Section 3.3.6):
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

# Contraction permutation of the key (See Section 3.3.7):
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,
7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,
33,52,45,41,49,35,28,31]

# Each integer here is the how much left-circular shift is applied
# to each half of the 56-bit key in each round (See Section 3.3.5):
shifts_key_halvs = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] 




###################################   S-boxes  ##################################

# Now create your s-boxes as an array of arrays by reading the contents
# of the file s-box-tables.txt:
with open('s-box-tables.txt') as f:
    arrays = []
    for line in f:
        if len(line) > 4:
            row = line.split()
                #print row
            
            arrays.append(row)
s_box = []
for i in range(0,32, 4):
    s_box.append([arrays[k] for k in range(i, i+4)]) # S_BOX

#print s_box
f.close

#######################  Get encryptin key from user  ###########################

def get_encryption_key(): # key                                                              
    ## ask user for input
    mykey = raw_input("Enter your 8 bytes key: ")
    ## make sure it satisfies any constraints on the key
    while not len(mykey) == 8 or not mykey.isalpha():
        print("Your key should be 8 English charaters.")
        mykey = raw_input("Enter your 8 bytes key: ")
        
    ## next, construct a BitVector from the key    
    user_key_bv = BitVector(textstring = mykey)   
    key_bv = user_key_bv.permute(key_permutation_1)        ## permute() is a BitVector function
    
    
    return key_bv


################################# Generatubg round keys  ########################
def extract_round_key( nkey ): # round key 
    round_key = []
    for i in range(16):
         [left,right] = nkey.divide_into_two()   ## divide_into_two() is a BitVector function
         ## 
         ##  the rest of the code
         ##

         left << shifts_key_halvs[i]
         right << shifts_key_halvs[i]
         nkey = left + right

         nkey.permute(key_permutation_2)
         round_key.append(nkey)

    return round_key


########################## encryption and decryption #############################

def des(encrypt_or_decrypt, input_file, output_file, key ): 
    bv = BitVector( filename = input_file ) 
    FILEOUT = open( output_file, 'w' ) 

    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file( 64 )   ## assumes that your file has an integral    
        
        mod = bitvec.length() % 64
        if not mod == 0:
            bitvec.pad_from_right(64 - mod)  ## multiple of 8 bytes. If not, you must pad it.
        
        [LE, RE] = bitvec.divide_into_two() 
        
        rkey = extract_round_key(key)
       
        for i in range(16):        
        ## write code to carry out 16 rounds of processing
            TMP = RE

            ## Expansion_permutation
            RE = RE.permute(expansion_permutation)
            # Get the order of key right
            if encrypt_or_decrypt == "encrypt":
                RE = RE ^ rkey[i]
            elif encrypt_or_decrypt == "decrypt":
                RE = RE ^ rkey[15 - i]
            ## Do the S_boxes subsititution
            firstbit = 0
            midbit = 1
            lastbit = 5
            newBV = BitVector(size = 0)
            for ct in range(8):
                row = 2 * RE[firstbit] + RE[lastbit]
                col = 8 * RE[midbit] + 4 * RE[midbit + 1] + 2 * RE[midbit + 2] + RE[midbit + 3]
                sbox_num = s_box[ct][row][col]
                sbox_bitvector = BitVector(intVal = int(sbox_num), size = 4)
                newBV += sbox_bitvector
                firstbit += 6
                midbit += 6
                lastbit += 6
            
            ## Permutation with P-Box
            newBV = newBV.permute(p_box_permutation)

            ## XOR with original LE
            RE = LE ^ newBV
            LE = TMP
        ## Add RE and LE up
        bitvec = RE + LE
        
        ## Output the encryption or decryption
        mytext = bitvec.get_text_from_bitvector()
        FILEOUT.write(mytext)
        print mytext

    FILEOUT.close()

#################################### main #######################################

def main():
    ## write code that prompts the user for the key
    ## and then invokes the functionality of your implementation

    ## get the key
    mykey = get_encryption_key()

    ## Ask for encryption or decryption
    while True:
        choice = raw_input("encrypt or decrypt? ")
        if choice == "encrypt":
            inputfile = "message.txt"
            outputfile = "encrypted.txt"
            break
        elif choice == "decrypt":
            inputfile = "encrypted.txt"
            outputfile = "decrypted.txt"
            break
            
    des(choice, inputfile, outputfile, mykey)

if __name__ == "__main__":
    main()

