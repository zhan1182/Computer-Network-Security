# Theory Problems
#
# 1. modulo addtion
#
# 2.
# Euclid's algorithm:   
#   gcd(1056, 348)
#       = gcd(348, 12)
#       = gcd(12, 0)
#
# Stein's algorithm
#   gcd(1056, 348)
#       = gcd(528, 174) x 2
#       = gcd(264, 87) x 2 x 2  = gcd(132, 87) x 4
#       = gcd(66, 87) x 4       = gcd(33, 87) x 4
#       = gcd(27, 33) x 4
#       = gcd(3, 27) x 4 
#       = gcd(12, 3) x 4        = gcd(6, 3) x 4
#       = gcd(3, 3) x 4         = 3 x 4 = 12
#
# Therefore, gcd(1056, 348) = 12
#
# 3. gcd(21, 34)
#       = gcd(34, 21)     residue 21 = 1x21 + 0x34
#       = gcd(21, 13)     residue 13 = -1x21 + 1x34
#       = gcd(13, 8)      residue 8  = 1x21 - 1x13 = 1x21 - (-1x21 + 1x34) = 2x21 - 1x34
#       = gcd(8, 5)       residue 5  = 1x13 - 1x8  = (-1x21 + 1x34) - (2x21 - 1x34) = -3x21 + 2x34
#       = gcd(5, 3)       residue 3  = 1x8 - 1x5   = (2x21 - 1x34) - (-3x21 + 2x34) = 5x21 - 3x34
#       = gcd(3, 2)       residue 2  = 1x5 - 1x3   = (-3x21 + 2x34) - (5x21 - 3x34) = -8x21 + 5x34
#       = gcd(2, 1)       residue 1  = 1x3 - 1x2   = (5x21 - 3x34) - (-8x21 + 5x34) = 13x21 - 8x34
# Therefore the multiplicative inverse of 21 modulo 34 is 13
#
# 4. Z14 =  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
#     MI =  -, 1, -, 5, -, 3, -, -, -, 11,  -,  9, -, 13
# Therefore, the non-zero elements that do not possess multiplicative inverses are 2, 4, 6, 7, 8, 10, 12
#
# 5. Examples:
#      gcd(4, 3) = 1 = 1x4 - 1x3  = -2x4 + 3x3
#      gcd(7, 4) = 1 = -1x7 + 2x4 = -5x7 + 9x4
#      gcd(12, 10) = 2 = 1x12 - 1x10 = -4x12 + 5x10
# 6. a. y = 12
#    b. y = 3
#    c. y = 4
#



# Programming Problem

# Function determines whether the num is prime or not
def isprime(num):
    for ct in range(2, num):
        if not num % ct:
            return False
    return True

# Entry point
if __name__ == "__main__":
    
    while True:
        # prompt the user to enter the number
        userinput = raw_input("Enter an integer, n is smaller than 50: ")
        try:
            num = int(userinput)
            if int(num) > 1  and int(num) < 50:
                break
            else:
                print("The integer should be positive and less than 50, try again")
        except ValueError:
            print("Please enter an integer, try again")
    
    fout = open("output.txt", "w")
    
    if isprime(num):
        print("field")
        fout.write("field")
    else:
        print("ring")
        fout.write("ring")

    fout.close()
