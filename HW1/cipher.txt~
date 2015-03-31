# open the files
fin = open("input.txt", "r")
fout = open("output.txt", "w")
fkey = open("key.txt", "r")

# read the content of the files
mytext = fin.read()  
mykey = fkey.read()

# get rid of the new line character  
textlen = len(mytext) - 1 
keylen = len(mykey) - 1
mytext = mytext[:textlen]
mykey = mykey[:keylen]

# make sure the key is longer or equal to the plaintext
while len(mykey) < len(mytext):
    mykey += mykey 

#print mykey
#print mytext

# begin to cipher
for ch in range(textlen):
    keyord = ord(mykey[ch])
    textord = ord(mytext[ch])
    # if the text character is lower case: change to upper case
    if textord >= 97 and textord <= 122:
        textout = textord - 32 + keyord - 97
        if textout > 90:
            textout -= 26
    # if the text character is upper case: change to lower case
    elif textord >= 65 and textord <= 90:
        textout = textord + 32 + keyord - 97
        if textout > 122:
            textout -= 26
    # write the ciphertext out
    fout.write(chr(textout))

# close the files
fin.close()
fout.close()
fkey.close()


# Test Cases:
#1:
#input.txt: canyoumeetmeatmidnightihavethegoods
#key.txt: abracadabra
#output.txt: CBEYQUPEFKMEBKMKDQIHYTIIRVGTKEHFODT

#2:
#input.txt: CANYOUMEETMEATMIDNIGHTIHAVETHEGOODS
#key.txt: abracadabra
#output.txt: cbeyqupefkmebkmkdqihytiirvgtkehfodt

#3:
#input.txt: IneedWATERandFood
#key.txt: aaaazzzz
#output.txt: iNEECvzserANCennd








