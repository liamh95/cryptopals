b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# str -> [int]
def hexStrToInt(hexString):
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
		if num<= 9:
			ret += chr(num+48)
		elif num>9 and num<=15:
			ret += chr(num+87)
		else:
			ret += "="
	return ret


# str -> str
def hexTo64(hexString):
	sanitized = hexStrToInt(hexString)
		// !--- Not spilling over properly ---!
	while len(sanitized)%3 != 0:
		sanitized.append(0)

	ret = ""
	i=0
	while len(ret)<len(sanitized)*2/3:
		ret += b64[(sanitized[3*i]<<2)+(sanitized[3*i+1]>>2)]
		ret += b64[((sanitized[3*i+1]&3)<<4)+sanitized[3*i+2]]
		i += 1

	return ret

