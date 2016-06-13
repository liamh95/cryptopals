#str -> [int]

$b64 = String.new("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")

def hexStrToInt(hexString)
	sanitized = hexString.split("")
	ret = Array.new
	sanitized.each do |i|
		asc = i.ord
		case asc
		when 48 .. 57
			ret << (asc-48)
		when 97 .. 122
			ret << (asc-87)
		else
			ret << 0
		end
	end
return ret
end

def intToHexStr(intArr)
	ret = ""
	intArr.each do |num|
		ret << num.to_s(16)
	end
	return ret
end

def hexTo64(hexString)
	sanitized = hexStrToInt(hexString)
	while (sanitized.length)%3 != 0
		sanitized << 0
	end
	ret = ""
	i=0
	while ret.length<(sanitized.length)*2/3
		ret << $b64[(sanitized[3*i]<<2)+(sanitized[3*i+1]>>2)]
		ret << $b64[((sanitized[3*i+1]&3)<<4)+sanitized[3*i+2]]
		i += 1
	end
	return ret
end

def fixedXOR(hexStr1, hexStr2)
	int1 = hexStrToInt(hexStr1)
	int2 = hexStrToInt(hexStr2)
	ret = Array.new
	for i in 0 ... int1.length
		ret << (int1[i]^int2[i])
	end
	return intToHexStr(ret)
end


