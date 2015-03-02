#!/usr/bin/env python

## extract_sshpubkey_params.py
## Author: Avi Kak
## Date: February 11, 2013

'''
An OpenSSH key consists of three fields:

  --- The key type            (ssh-rsa in my case)

  --- A chunk of PEM-encoded data

  --- A comment

The three fields are separated by a white space character.

The important information, meaning the public exponent and the
modulus, are stored in the PEM-encoded chunk in the form of (length,
data) pairs, where is length is encoded as four bytes (in big-endian
order).  There are three of these (length, data) pairs in the
PEM-encoded chunk:

    1)   algorithm name     one of ssh-rsa or ssh-dsa   (this really
                            duplicates the key type at the beginning of
                            the public key file)

    2)   RSA public exponent

    3)   RSA private exponent

The code shown below reads in the PEM chunk, does Base64 decoding of
the chunk, and then walks through the chunk as it partitions it
according to the (length, data) pairs.  So it will look at the first
four bytes to figure out how many bytes to read next for the algorithm
name.  After that it will look at the next four bytes to figure out
how many bytes to examine for the public exponent, etc.
'''

import sys
import base64
import BitVector

if len(sys.argv) != 2:
    sys.stderr.write("Usage: %s   <public key file>\n" % sys.argv[0])
    sys.exit(1)

keydata = base64.b64decode(open(sys.argv[1]).read().split(None)[1])
bv = BitVector.BitVector( rawbytes = keydata )

parts = []
while bv.length() > 0:
  bv_length = int(bv[:32])               # read 4 bytes for length of data
  data_bv = bv[32:32+bv_length*8]        # read the data
  parts.append(data_bv)               
  bv.shift_left(32+bv_length*8)          # shift the starting BV and
  bv = bv[0:-32-bv_length*8]             #    and truncate its length

public_exponent = int(parts[1])
modulus = int(parts[2])

print "public exponent: ", public_exponent
print "modulus: ", modulus

