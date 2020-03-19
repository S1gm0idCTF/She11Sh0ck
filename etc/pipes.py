from etc.encryptions import *

pipe = " | " 
class ProcessPipe():
	def __init__(self, command):
		operations = 0
		print(command)
		self.stack = command.split(pipe)
		cmd = self.stack[0]
		
		while len(self.stack) > 0:
			
			print("processing: " + self.stack[0])

			if operations == 0:
				#extractString()
				a = cmd.find('-')
				b = cmd[a:].find(" ")+a

				operation = cmd[0:a-1]
				f = cmd[a:b]
				self.string = cmd[b+1:]
				print(self.string)
				self.doOperation(operation,f)
			else:
				print(self.string)
				c = self.stack[0].split(" ")
				self.doOperation(c[0],c[1])
				print(c[0],c[1])
			self.removeCommandFromStack()
			operations = operations + 1 
	def doOperation(self, operation, f):
		print(self.string)
		if operation == "hex":
			self.string = do_hex(f, self.string)
		if operation == "b16":
			self.string = do_b16(f, self.string)
		if operation == "b32":
			self.string = do_b32(f, self.string)
		if operation == "b64":
			self.string = do_b64(f, self.string)
		if operation == "binary":
			self.string = do_binary(f, self.string)
		if operation == "az26":
			self.string = do_az26(f, self.string)
	def removeCommandFromStack(self):
		self.stack = self.stack[1:]
	def getString(self):
		return self.string

#command = "base64 -dde | base64 -eed | base64 -e | base64 -e | base64 -eed | base64 -eed | base64 -eed "


#UsAgE:
#if pipe in command:              
#pc = ProcessPipe(command)





