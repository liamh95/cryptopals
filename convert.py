import collections
b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def asciiToHex(ascStr):
    ret = ""
    for char in ascStr:
        ret += hex(ord(char))[2:]
    return ret

# str -> [int]
def hexStrToInt(hexString):
	sanitized = hexString.lstrip("0x")
	ret = []
	for char in hexString:
		asc = ord(char)
		if asc>=48 and asc<=57:
			ret.append(asc-48)
		elif asc>=97 and asc<=122:
			ret.append(asc-87)
		else:
			ret.append(0)
	return ret

# [int] -> str
def intToHexStr(intArr):
	ret = ""
	for num in intArr:
		ret += hex(num)[2:]
	return ret


# str -> str
def hexTo64(hexString):
	sanitized = hexStrToInt(hexString)
	while len(sanitized)%3 != 0:
		sanitized.append(0)

	ret = ""
	i=0
	while len(ret)<len(sanitized)*2/3:
		ret += b64[(sanitized[3*i]<<2)+(sanitized[3*i+1]>>2)]
		ret += b64[((sanitized[3*i+1]&3)<<4)+sanitized[3*i+2]]
		i += 1

	return ret

def fixedXOR(hexStr1, hexStr2):
	int1 = hexStrToInt(hexStr1)
	int2 = hexStrToInt(hexStr2)
	ret = []
	for i in range(0, len(int1)):
		ret.append(int1[i]^int2[i])
	return intToHexStr(ret)

# take hex chars in pairs -> ascii table
def hexStrToASCII(hexStr):
	intArr = hexStrToInt(hexStr)
	if len(intArr)%2 != 0:
		intArr.append(0)	
	# form new array from pairs
	paired = []
	for i in range(0, len(intArr)/2):
		paired.append( (16*intArr[2*i])+intArr[2*i+1] )
	ret = ""
	for num in paired:
		ret += chr(num)
	return ret

# ASCII -> Bool
def plausible(inStr, tolerance):
	sanitize = inStr.lower().replace(" ","")
	top = collections.Counter(sanitize).most_common(5)
	score = 0
	for entry in top:
		if entry[0]=='r' or entry[0]=='e' or entry[0]=='t' or entry[0]=='a' or entry[0]=='o' or entry[0]=='i' or entry[0]=='n' or entry[0]=='s':
			score += 1
	return True if score>=tolerance else False

# (ASCII String, ASCII String) -> hex String
def repeatingKeyXOR(inStr, key):
    i=0
    ret = ""
    while i<len(inStr):
        app = hex(ord(inStr[i])^ord(key[i%len(key)]))
        if int(app, 16)<int("10", 16):
            ret += "0"
        ret+=app[2:]
        i += 1
    return ret
