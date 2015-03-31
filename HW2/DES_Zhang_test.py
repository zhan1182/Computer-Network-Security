import sys
from BitVector import *

if __name__ == "__main__":
    """
    arrays = []
    #ct = 1
    with open('s-box-tables.txt') as f:
        for line in f:
            if len(line) > 4:
                row = line.split()
                #ct = ct + 1
                #print row

                arrays.append(row)
#print ct

    #print arrays
    """            
    firstbit = 0
    midbit = 1
    lastbit = 5
    newRE = []
    for ct in range(8):
        #row = 2 * RE[firstbit] + RE[lastbit]
        #col = 8 * RE[midbit] + 4 * RE[midbit + 1] + 2 * RE[midbit + 2] + RE[midbit + 3]
        #Sbox_num = S_box[ct][row][col]
        newRE.append(BitVector(intVal = 3, size = 4))
        firstbit += 6
        midbit += 6
        lastbit += 6
    
#print firstbit - 6
#print midbit - 6
#print lastbit - 6
        print newRE
