import collections
inF = open("8.txt", "r")
lineNo=1
for line in inF:
	hextext = line.rstrip('\n')
	blocks = [hextext[i:i+32] for i in range(0, len(hextext), 32)]
	numDupes = len(blocks) - len(set(blocks))
	if numDupes>0:
		dupe = collections.Counter(blocks).most_common(1)
		print("Dupe found in line "+ str(lineNo))
		print("Number of dupes: "+str(numDupes))
		print(dupe[0][0])
	lineNo += 1
inF.close()