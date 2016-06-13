import convert

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

tst = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
print repeatingKeyXOR(tst, "ICE")

