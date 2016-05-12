from hexTo64 import intToHexStr, hexStrToInt

def fixedXOR(hexStr1, hexStr2):
	int1 = hexStrToInt(hexStr1)
	int2 = hexStrToInt(hexStr2)
	ret = []
	for i in range(0, len(int1)):
		ret.append(int1[i]^int2[i])
	return intToHexStr(ret)
str1 = "1c0111001f010100061a024b53535009181c"
str2 = "686974207468652062756c6c277320657965"
print(fixedXOR(str1,str2))
