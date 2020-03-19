import base64


#
def do_hex(f, input):
	s = ""
	if f == "-e" or f == "-encode":
		hex = (base64.b16encode(input.encode()).decode("utf-8"))
		while len(hex) >= 2:
			s = s + hex[0:2] + " "
			hex = hex[2:]
		return s.strip()
	
	if f == "-d" or f == "-decode":
		input = input.replace(" ", "")
		return (base64.b16decode(input).decode("utf-8"))
#
def do_b16(f, input):
	if f == "-e" or f == "-encode":
		return (base64.b16encode(input.encode()).decode("utf-8"))
	if f == "-d" or f == "-decode":
		return (base64.b16decode(input).decode("utf-8"))
#
def do_b32(f, input):
	if f == "-e" or f == "-encode":
		return (base64.b32encode(input.encode()).decode("utf-8"))
	if f == "-d" or f == "-decode":
		return (base64.b32decode(input).decode("utf-8"))
#
def do_b64(f, input):
	if f == "-e" or f == "-encode":
		return (base64.b64encode(input.encode()).decode("utf-8"))
	if f == "-d" or f == "-decode":
		return (base64.b64decode(input).decode("utf-8"))
##
def do_binary(f, input):
	if f == "-e" or f == "-encode":
		return ' '.join(bin(ord(char)).split('b')[1].rjust(8, '0') for char in input)

	if f == "-d" or f == "-decode":
		input = input.replace(' ', '')
		input = " ".join(input[i:i+8] for i in range(0, len(input), 8))
		return ''.join(chr(int(binary, 2)) for binary in input.split(' '))
##
def do_az26(f, input):
	output = ""
	input = input.upper()
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if f == "-e" or f == "-encode":
		input = input.replace(" ","")
		for char in input:
			if alphabet.find(char) > -1:
				output = output + " " + str(alphabet.find(char)+1)
			else:
				raise Exception('Invalid Arguments', 'AZ26 Cipher')
		return output[1:]
	if f == "-d" or f == "-decode":
		for i in input.split(" "):
			try:
				i = int(i)
				output = output + alphabet[int(i)-1]
			except:
				raise Exception('Invalid Arguments', 'AZ26 Cipher')
		return output
##
def do_atbash(f, input):
	output = ""
	input = input.upper()
	alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	revalpha = alpha[::-1]
	if f == "-e" or f == "-encode" or f == "-d" or f == "-decode":
		for char in input:
			if alpha.find(char) > -1:
				output = output + "" + revalpha[alpha.find(char)]
			elif char == " ":
				output = output + " "
			else:
				raise Exception('Invalid Arguments', 'atbash Cipher')
	return output
##
def do_trans(f, input):
	output = ""
	if f == "-upper":
		output = input.lower()
	if f == "-lower":
		output = input.upper()
	if f == "-join":
		output = input.replace(" ", "")
	if f == "-rev" or f == "-reverse":
		output = input[::-1]
	if f.startswith("-s"):
		try:
			x = int(f.replace("-s", ""))
			while len(input) >= x:
				output = output + input[:x] + " "
				input = input[x:]

		except:
			raise Exception('Invalid Arguments', '-s[int]')
	
	return output
##Future implementation... ASCII... Various Ciphers (rail ciphers?)... 