from __future__ import print_function
import convert, itertools


def hamming(str1, str2):
    if len(str1) != len(str2):
        return -1
    zipped = zip(str1, str2)
    ret = 0
    for pair in zipped:
        xor = ord(pair[0])^ord(pair[1])
        while xor != 0:
            ret += 1
            xor &= xor-1
    return ret

def b64ToHex(b64String):
    intArr = []
    for char in b64String:
        intArr.append(convert.b64.find(char))
    ret = ""
    i=0
    while len(ret)<len(b64String)*3/2:
        ret += hex(intArr[2*i]>>2)[2:]
        ret += hex(4*(intArr[2*i]&3)+(intArr[2*i+1]>>4))[2:]
        ret += hex(intArr[2*i+1]&15)[2:]
        i+=1
    return ret

def b64ToASCII(b64String):
    intArr = []
    for char in b64String:
        if char == '=':
            intArr.append(0)
        else:
            intArr.append(convert.b64.find(char))
    ret = ""
    i=0
    while len(ret)<len(b64String)*3/4:
        ret += chr( (intArr[4*i]<<2) + (intArr[4*i+1]>>4) )
        ret += chr( ((intArr[4*i+1]&15)<<4) + (intArr[4*i+2]>>2) )
        ret += chr( ((intArr[4*i+2]&3)<<6) + intArr[4*i+3] )
        i += 1
    return ret

# ([int], ASCII char) -> ASCII
def intXORtoASCII(inNums, keyChar):
    ret = ""
    for num in inNums:
        ret += chr(num^ord(keyChar))
    return ret

#(ASCII str, ASCII char) -> ASCII str
def ASCIIXOR(instr, keyChar):
    ret=""
    for char in instr:
        ret += chr(ord(char)^ord(keyChar))
    return ret
    
###############################################################
rawText = ""
# Take in base64 string from file
with open("6.txt", 'r') as inF:
    for line in inF:
        rawText += line.rstrip('\n')
inF.close()
# convert base64 to one long ASCII string
plainCipher = b64ToASCII(rawText)

# probable key sizes
sizes = []
normedDists = []
for KEYSIZE in range(2, 41):
    blocks = [plainCipher[n*KEYSIZE:(n+1)*KEYSIZE] for n in range(0,4)]
    if len(blocks[-1])<KEYSIZE:
        break
    hams = list(itertools.starmap(hamming, zip(blocks, blocks[1:])))
    avgHam = float(sum(hams))/len(hams)/KEYSIZE
    normedDists.append(avgHam)
    sizes.append(KEYSIZE)



#sort by Hamming distance
zipped = zip(sizes, normedDists)
zipped.sort(key = lambda t: t[1])
#print(zipped)
#print(str(hamming("this is a test", "wokka wokka!!!")))



# outF = open("out.txt", 'a')
# outF.write(rawText)
# outF.close()

#ASCII string -> [int]
#cipherNums = [ord(char) for char in plainCipher]

for i in range(0,3):
    KEYSIZE = zipped[i][0]
    
    #Pad according to KEYSIZE
    #numcpy = list(cipherNums)
    strcpy = plainCipher
    #while len(numcpy)%KEYSIZE != 0:
    while len(strcpy)%KEYSIZE != 0:
        #numcpy.append(0)
        strcpy += '\0'
    
    #blockSize = len(numcpy)/KEYSIZE
    numBlocks = len(strcpy)/KEYSIZE
    #blocks = [[]  for m in range(0,KEYSIZE)]
    cipherBlocks = [strcpy[j::KEYSIZE] for j in range(0,KEYSIZE)]
    #for j in range(0, len(numcpy)):
    #    blocks[j%KEYSIZE].append(numcpy[j])
    
#     #Single XOR blocks
#     #keyPossibilities = [[] for n in range(0,KEYSIZE)]
    
    #lists of lists
    keyPossibilities = []
    decipheredBlocks = []

    for block in cipherBlocks:
        charPossibilities = []
        blockPossibilities = []
        for l in range(32, 123):
            testStr = ASCIIXOR(block, chr(l))
            if convert.plausible(testStr, 3):
                charPossibilities.append(chr(l))
                blockPossibilities.append(testStr)
        keyPossibilities.append(charPossibilities)
        decipheredBlocks.append(blockPossibilities)


# #     for k in range(0, KEYSIZE):
# #         for l in range(0, 256):
# #             testStr = intXORtoASCII(blocks[k], chr(l))
# #             if convert.plausible(testStr, 3):
# #                 keyPossibilities[k].append(chr(l))
# #                 testStrings[k].append(testStr)

    charProd = list(itertools.product(*keyPossibilities))
    blockProd = list(itertools.product(*decipheredBlocks))
    #outF.write("-----KEYSIZE = "+str(KEYSIZE)+"-----\n")
    print("-----KEYSIZE = "+str(KEYSIZE)+"-----")
    for char in keyPossibilities:
        print("("+str(len(char))+")", end="")
    print()
    for char in keyPossibilities:
        print(char)

#     # for it in range(0, len(charProd)):
#     #     key=""
#     #     message = ""
#     #     for char in charProd[it]:
#     #         key+= char
#     #     for ind in range(0, blockSize):
#     #         for indd in range(0, KEYSIZE):
#     #             message+=blockProd[it][indd][ind]
#     #     outF.write("Key: "+key+"\n")
#     #     outF.write("Message: "+message+"\n")
#         #print("Key "+key)
#         #print("Message: "+message+"\n")
