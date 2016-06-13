import convert, collections

# ASCII -> Bool
def plausible(inStr, tolerance):
	sanitize = inStr.lower().replace(" ", "")
	frequencies = collections.Counter(inStr)
	top = frequencies.most_common(5)
	score = 0
	for entry in top:
		if entry[0]=='e' or entry[0]=='t' or entry[0]=='a' or entry[0]=='o' or entry[0]=='i' or entry[0]=='n' or entry[0]=='s':
			score += 1
	return True if score>=tolerance else False

###########################################

encrypted = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
plausibles = []
for i in range(0, 256):
	char = convert.intToHexStr([i])
	hexed = char*(len(encrypted)/len(char))
	xor = convert.fixedXOR(hexed, encrypted)
	testStr = convert.hexStrToASCII(xor)
	if plausible(testStr):
		plausibles.append(testStr+" - "+chr(i))
for message in plausibles:
	print(message)

