from __future__ import print_function

#SBox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
#0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
#0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
#0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07]


def xtime(inByte):
    ret = inByte
    ret <<= 1
    if ret>=256:
    	ret ^= 283
    return ret

def F256mult(byte1, byte2):
    temp1=byte1
    temp2=byte2
    ret = 0
    while temp2>0:
    	if temp2%2==1:
    		ret ^= temp1
    	temp1 = xtime(temp1)
    	temp2 >>= 1
    return ret

def degree(byte):
    temp = byte
    deg = -1
    while temp!=0:
        temp >>=1
        deg += 1
    return deg

def byteToPoly(byte):
    if byte==0:
        return '0'
    ret = ""
    temp = byte
    deg = 0
    while temp>0:
        if temp%2==1:
            tempstr = "+1"+ret if deg==0 else "+x^"+str(deg)+ret
            #tempstr = "+x^"+str(deg)+ret
            ret = tempstr
        deg += 1
        temp >>=1
    ret = ret.lstrip("+")
    return ret

#multiplication of elements in Z2[x]
def Z2xMult(byte1, byte2):
    temp1=byte1
    temp2=byte2
    ret = 0
    while temp2>0:
	if temp2%2==1:
	    ret ^= temp1
	temp1 <<= 1
	temp2 >>= 1
    return ret

modByte = 283
def setMod(byte):
    modByte = byte

def Z2xDiv(byteA, byteB):
    r = byteA
    q = 0
    degMax = degree(byteB)
    while degree(r)>=degMax:
        d = degree(r)
        v = 2**(d-degMax)
        r ^= Z2xMult(v,byteB)
        q ^= v
    return [q, r]

def Z2xExtended(byteA, byteB):
    if byteB==0:
        return [1, 0, byteA]
    else:
        u = 1
        d = byteA
        v1 = 0
        v3 = byteB
        while v3 != 0:
            [q, t3] = Z2xDiv(d,v3)
            t1  = u ^ Z2xMult(q,v1)
            u = v1
            d = v3
            v1 = t1
            v3 = t3
        v = Z2xDiv(d^Z2xMult(byteA,u), byteB)[0]
        return [u, v, d]

def F256invert(byte):
    if byte==0 or byte==283:
        return 0
    else:
        return Z2xExtended(byte, 283)[0]

def polyMult(a, b):
	d0 = F256mult(a[0], b[0])^F256mult(a[3],b[1])^F256mult(a[2], b[2])^F256mult(a[1],b[3])
	d1 = F256mult(a[1], b[0])^F256mult(a[0],b[1])^F256mult(a[3], b[2])^F256mult(a[2],b[3])
	d2 = F256mult(a[2], b[0])^F256mult(a[1],b[1])^F256mult(a[0], b[2])^F256mult(a[3],b[3])
	d3 = F256mult(a[3], b[0])^F256mult(a[2],b[1])^F256mult(a[1], b[2])^F256mult(a[0],b[3])
	return [d0, d1, d2, d3]

def printGrid(grid):
    for i in range(0,len(grid)):
        print(grid[i], end = " ")
        if i%4 ==3:
            print()

c = 0x63
def makeSBox():
    SBox = []
    for byte in range(0, 256):
        invByte = F256invert(byte)
        boxByte = 0
        # eqn (5.1)
        for i in range(0,8):
            bit = ((invByte>>i)%2) ^ ( (invByte>>((i+4)%8))%2 ) ^ ( (invByte>>((i+5)%8))%2 ) ^ ( (invByte>>((i+6)%8))%2 ) ^ ( (invByte>>((i+7)%8))%2 ) ^ ( (c>>i)%2 )
            boxByte += (bit<<i)
        SBox.append(boxByte)
    return SBox

# 5.1.1
# SubBytes()
def SubBytes(state):
    for i in range(0,len(state)):
        state[i] = SubBytes[state[i]]

# 5.1.2
# ShiftRows()
def ShiftRows(state):
    temp = 0
    for row in range(1,4):
        temp = state[4*row:4*(row+1)]
        for col in range(0,4):
            state[4*row+col] = temp[(col+row)%4]

# 5.1.3
# MixColumns()
def MixColumns(state):
    for col in range(0,4):
        temp = [state[4*n+col] for n in range(0,4)]
        state[0 +col] = F256mult(0x02, temp[0]) ^ F256mult(0x03, temp[1]) ^ temp[2] ^ temp[3]
        state[4 +col] = temp[0] ^ F256mult(0x02, temp[1]) ^ F256mult(0x03, temp[2]) ^ temp[3]
        state[8 +col] = temp[0] ^ temp[1] ^ F256mult(0x02, temp[2]) ^ F256mult(0x03, temp[3])
        state[12+col] = F256mult(0x03, temp[0]) ^ temp[1] ^ temp[2] ^ F256mult(0x02, temp[3])

# 5.1.4
# AddRoundKey()
def AddRoundKey(state, schedBlock):
    for i in range(0,len(state)):
        state[i] ^= schedBlock[i]

##################################################
#              5.2  Key Expansion                #
##################################################