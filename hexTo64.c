#include<stdio.h>
#include<stdlib.h>
#include<string.h>

//base64 indexing (Wikipedia)
char* b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

/* char* hexString: input string of hexadecimal values
 *
 * Returns base64 representation of hexString.
 * For every 3 hex characters we get 2 base64 characters.
 * Obtain bas64 string by shifting bits.
 */
unsigned char* decrypt(unsigned char* hexString){
	//start by sanitizing the input: get a string with length
	//	divisible by 3
	unsigned char* sanitized;
	int inSize = strlen(hexString);
	//if the input length is divisible by 3, no need to pad
	if(inSize%3==0)
		sanitized = hexString;
	//Pad length of input so that it's divisible by 3
	//	!-- NOT TESTED YET --!
	else{
		//sanitized input begins the same way as hexString
		//(inSize+2)/3 = ceil(inSize/3)
		sanitized = (unsigned char*)malloc(sizeof(char)*((inSize+2)/3+1));
		memcpy(sanitized, hexString, inSize);
		
		//Fill rest of string with 0's
		int i;
		for(i=inSize; i<strlen(sanitized); i++)
			sanitized[i]= 0x0;
	}

	int sanitizedLen = strlen(sanitized);
	//return string has 2 chars for every 3 input chars
	int retLen = sanitizedLen*2/3;
	//+1 for terminating nullchar
	unsigned char* ret = (unsigned char*)malloc((retLen+1)*sizeof(char));
	
	//bit shifting
	int i;
	for(i=0; i<retLen/2; i++){		
		//shift 6 left first to chop off 6 most significant bits
		unsigned char temp = sanitized[3*i+1]<<6;

		//fairly certain this line works as intended
		ret[2*i] = b64[(sanitized[3*i]<<2)+(sanitized[3*i+1]>>2)];
		
		//pretty sure the problem is here
		ret[2*i+1] = b64[(temp>>2)+sanitized[3*i+2]];
	}
	return ret;
}

int main(){
	//test string. first 9 chars from the one that appears on 
	//	the cryptopals problem description here
	//	http://cryptopals.com/sets/1/challenges/1
	unsigned char in[12] = {0x4, 0x9, 0x2, 0x7, 0x6, 0xd, 0x2, 0x0, 0x6, 0xb, 0x6, 0x9};
	
	//prints "SSdsIA"
	printf("%s", decrypt(in));

	//first 3 characters are correct. fourth is 1 index short.
	//	fifth is correct, sixth is straight wrong.
	return 0;
}

