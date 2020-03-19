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


##Future implementation... ASCII... Various Ciphers (rail ciphers?)... 