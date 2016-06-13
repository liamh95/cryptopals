import convert, collections

with open("4.txt") as f:
	lines = [line.rstrip("\n") for line in f]

lineNo=1
for line in lines:
	plausibles = []
	for i in range(0, 256):
		char = convert.intToHexStr([i])
		hexed = char*(len(line)/len(char))
		xor = convert.fixedXOR(hexed, line)
		testStr = convert.hexStrToASCII(xor)
		if convert.plausible(testStr, 3):
			plausibles.append(testStr+" - "+str(lineNo)+" - "+chr(i))
	for message in plausibles:
		print(message)
	lineNo += 1

