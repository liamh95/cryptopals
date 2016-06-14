def pkcs7Pad(inStr, padTo):
	l = len(inStr)
	if l>padTo or padTo>256:
		return ""
	else:
		ret = inStr
		while len(ret)<padTo:
			ret += chr(padTo-l)
	return ret