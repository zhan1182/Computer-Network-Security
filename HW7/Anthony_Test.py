
import sys
from BitVector import *

# initialize the hash buffer
a = BitVector(hexstring = '6a09e667f3bcc908')
b = BitVector(hexstring = 'bb67ae8584caa73b')
c = BitVector(hexstring = '3c6ef372fe94f82b')
d = BitVector(hexstring = 'a54ff53a5f1d36f1')
e = BitVector(hexstring = '510e527fade682d1')
f = BitVector(hexstring = '9b05688c2b3e6c1f')
g = BitVector(hexstring = '1f83d9abfb41bd6b')
h = BitVector(hexstring = '5be0cd19137e2179')
o_a = a.deep_copy()
o_b = b.deep_copy()
o_c = c.deep_copy()
o_d = d.deep_copy()
o_e = e.deep_copy()
o_f = f.deep_copy()
o_g = g.deep_copy()
o_h = h.deep_copy()
# initialize K (jeezus)
K = [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]


# initialize message blocks
# find number of bytes in file
input_text = open(sys.argv[1], 'r+').read()
num_bytes = len(input_text)


# initialize array of bitvectors for each plaintext block
plaintextlist = (num_bytes/128 + 1) * [0]
bv = BitVector(filename = sys.argv[1])

for i in range(len(plaintextlist)):
    plaintextlist[i] = bv.read_bits_from_file(1024)
    # need add 128 bits plus the 1 bit
    # need to retain multiple of 1024
if(len(plaintextlist[-1]) > 895):
    plaintextlist[-1].pad_from_right(1024 - len(plaintextlist[-1]))
    one = BitVector(intVal = 1)
    one.pad_from_right(895)
    plaintextlist.append(one + BitVector(intVal = num_bytes * 8, size = 128))
else:
    one = BitVector(intVal = 1)
    one.pad_from_right(1024- len(plaintextlist[-1]) - 129)
    message_len = one + BitVector(intVal = num_bytes*8 , size = 128)
    plaintextlist[-1] = plaintextlist[-1] + message_len


hash_message = BitVector(size = 0)
hash_block = []
# process each 1024 bit message block
for block in plaintextlist:
    a = o_a.deep_copy()
    b = o_b.deep_copy()
    c = o_c.deep_copy()
    d = o_d.deep_copy()
    e = o_e.deep_copy()
    f = o_f.deep_copy()
    g = o_g.deep_copy()
    h = o_h.deep_copy()
    # generate 80, 64 bit words
    # first 16 words are from block
    words = [0] * 80
    words[0:16] = [block[x:x+64] for x in range(0, 1024, 64)]
    print words[1].shift_right(7)

    # generate next 64, 64 bit words
    for i in range(16,80):
        theta_0_x = (words[i-15] >> 1) ^ (words[i-15] >> 8) ^ words[i-15].shift_right(7)
        theta_1_x = (words[i-2] >> 19) ^ (words[i-2] >> 61) ^ words[i-2].shift_right(6)
        words[i] = BitVector(intVal = (((int(words[i-16]) + int(theta_0_x)) % (2 ** 64)) + ((int(words[i-7]) + int(theta_1_x)) % (2 ** 64))) % (2 ** 64), size = 64)

    for i in range(80):
    # implement the round function
        Ch_efg = (e & f) ^ (~e & g)
        Maj_abc = (a & b) ^ (a & c) ^ (b & c)
        a_copy = a.deep_copy()
        sum_a = (a_copy >> 28) ^ (a_copy >> 34) ^ (a_copy >> 39)
        e_copy = e.deep_copy()
        sum_e = (e_copy >> 14) ^ (e_copy >> 18) ^ (e_copy >> 41)
        T_1 = (((((int(h) + int(Ch_efg)) % (2 ** 64)) + int(sum_e)) % (2 ** 64)) + ((int(words[i]) + int(K[i])) % (2 ** 64))) % (2 ** 64)
        T_2 = (int(sum_a) + int(Maj_abc)) % (2 ** 64)
        h = g
        g = f
        f = e
        e = BitVector(intVal = (int(d) + int(T_1)) % (2**64), size = 64)
        d = c
        c = b
        b = a
        a = BitVector(intVal = (int(T_1) + int(T_2)) % (2**64), size = 64)


    h_a = BitVector(intVal = (int(a) + int(o_a)) % (2 ** 64), size = 64)
    h_b = BitVector(intVal = (int(b) + int(o_b)) % (2 ** 64), size = 64)
    h_c = BitVector(intVal = (int(c) + int(o_c)) % (2 ** 64), size = 64)
    h_d = BitVector(intVal = (int(d) + int(o_d)) % (2 ** 64), size = 64)
    h_e = BitVector(intVal = (int(e) + int(o_e)) % (2 ** 64), size = 64)
    h_f = BitVector(intVal = (int(f) + int(o_f)) % (2 ** 64), size = 64)
    h_g = BitVector(intVal = (int(g) + int(o_g)) % (2 ** 64), size = 64)
    h_h = BitVector(intVal = (int(h) + int(o_h)) % (2 ** 64), size = 64)


    hash_message = h_a + h_b + h_c + h_d + h_e + h_f + h_g + h_h
    hash_hex_string = hash_message.getHexStringFromBitVector()
    hash_block.append(hash_hex_string)


with open('output.txt', 'wa') as f:
    for hex_string in hash_hex_string:
        f.write(hex_string)