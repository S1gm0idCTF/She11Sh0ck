import discord
from errors import sendErrorMessage
from etc.betterEmbeds import sendEmbed
from discord.ext import commands
from datetime import datetime

class processMessages():
	def __init__(self, messages):
		self.messages = [x for x in messages][::-1]
		self.formattedMessages = self.findCodeBlocks()
	def getMessages(self):
		return self.formattedMessages
	def findCodeBlocks(self):
		formattedMessages = []
		for msg in self.messages:
			message = msg.content
			finalTextAppension = "" 
			if message.count("`") % 2 == 0 and message.count("`") > 0:
				while "````" in message:
					message = message.replace("````", "")
				while "``````" in message:
					message = message.replace("``````", "")
				while "```" in message:
					message = message.replace("```", "ﻼ")
				while "``" in message:
					message = message.replace("``", "ﻼ")
				message = message.replace("`", "ﻼ")

				codeblockIndex = [pos+1 for pos, char in enumerate(message) if char == 'ﻼ']
				#print(codeblockIndex)
				if codeblockIndex[0] != 0:
					#if the there's text between first message, and `
					formattedMessages.append(embedsObj(message[0:(codeblockIndex[0]-1)],"text"))
					#print("t:" + str(message[0:(codeblockIndex[0]-1)]))

				if codeblockIndex[::-1][0] != len(message):
					#append any text after codeblock...  `
					finalTextAppension = message[codeblockIndex[::-1][0]:]

				while len(codeblockIndex) > 1:
					#print(codeblockIndex[0],codeblockIndex[1])
					substr = message[codeblockIndex[0]:codeblockIndex[1]-1]
					formattedMessages.append(embedsObj(substr,"codeblock"))
					#print(">>" + substr)
					if len(codeblockIndex) > 2:
						if message[codeblockIndex[1]:codeblockIndex[2]-1].replace(" ", "").replace("\n", "") != "":
							formattedMessages.append(embedsObj(substr,"text"))
							#print("t:" + message[codeblockIndex[1]:codeblockIndex[2]-1] + ":")
					codeblockIndex = codeblockIndex[2:]
					#append any text after codeblock...  `
					if finalTextAppension != "":
						formattedMessages.append(embedsObj(finalTextAppension,"text"))
						
			else:
				formattedMessages.append(embedsObj(message, "text"))
			if msg.attachments != []:
				for attchmnt in msg.attachments:
					acceptableImageTypes = ['.png', '.jpg', '.jpeg', '.gif'] 
					if attchmnt.url[attchmnt.url.rfind("."):] in acceptableImageTypes:
						formattedMessages.append(embedsObj(".", "file-img", attchmnt.url))
					else:
						formattedMessages.append(embedsObj(".", "file-other", attchmnt.url))
					
					
					
					
		return formattedMessages

class betterEmbeds():
	def __init__(self, category):
		self.embed = discord.Embed(title="# {}".format(str(category)),description="### Created: {}".format(str(datetime.now())),color=0xFF0000)
		self.destination = ''
		self.length = 0
		self.objectCount = 0
		self.imageCount = 0
	async def test_embed(self, bodyLength):
		if (self.length + bodyLength >= 5500) or (self.objectCount + 1 >= 12):
			return False
		else:
			return True

	async def reInitialize(self,textChannelName):
		self.embed = discord.Embed(title="\n",description="\n",color=0xFF0000)
		self.length = 0
		self.objectCount = 0
		self.imageCount = 0

	async def add_field(self, textChannelName, body):
		if len(body) < 3:
			return
		if not await self.test_embed(len(body)):
			if self.destination != '':
				await self.send_message()
				await self.reInitialize(str(textChannelName))
		self.length = self.length + len(body)
		self.objectCount = self.objectCount + 1
		self.embed.add_field(name=str("### " + textChannelName),value=body + "\n", inline=False)
	async def add_image(self,textChannelName, body):
		if len(body) < 3:
			return
		if not await self.test_embed(len(body)):
			if self.destination != '':
				await self.send_message()
				await self.reInitialize(str(textChannelName))
		if self.imageCount >= 1:
			if self.destination != '':
				await self.send_message()
				await self.reInitialize(str(textChannelName))
		self.imageCount = 1
		self.length = self.length + len(body)
		self.objectCount = self.objectCount + 1
		self.embed.set_image(url=body)

	async def add_destination(self,destination):
		#print("Destination SET: " + str(destination))
		self.destination = destination

	async def send_message(self):
		await self.destination.send(embed=self.embed)

def findI(message):
	i = -1
	lb = 500 # lower-bound
	
	i = message[lb:850].rfind('\n')
	if i == -1:
		i = message[lb:850].rfind(' ')	
	if i == -1:
		i = 300
	#print(lb, i, lb+i)
	return lb + i
		
			
async def splitTextMessage(message, textChannel,embed):
	
	message = message['content']
	while len(message) > 950:
		i = findI(message)
		await embed.add_field(str(textChannel.name), message[0:i])
		message = message[i:]
	await embed.add_field(str(textChannel.name), message)

#async def splitCodeMessage(message, textChannel,embed):
	
	#message = message['content']
	#while len(message) > 950:
		#i = findI(message)
		#await embed.add_field(str(textChannel.name), message[0:i])
		#message = message[i:]
#	await embed.add_field(str(textChannel.name), message)

async def splitCodeMessage(message, textChannel, embed):

	message = message['content']
	acceptableLanguages = ["js", "javascript", "python", "c", "c++", "go", "rust"] # <---------------- add any desired languages here... 
	
	language = message[0:min(message.find("\n"), 32)]
	if language not in acceptableLanguages: 
		language = ""
	#print("LANG: " + language)

	while len(message) > 950:
		i = findI(message)
		if not (message.startswith(language+str("\n")) and language != ""):
			message = language+("\n") + message
		await embed.add_field(str(textChannel.name), "```{}```".format(message[0:i]))
		message = message[i+1:]
	if not (message.startswith(language+str("\n")) and language != ""):
		message = language+("\n") + message
	await embed.add_field(str(textChannel.name), "```{}```".format(message))

def embedsObj(content, msgType, attachment=None):
	acceptableMsgTypes = ['text', 'codeblock', 'link', 'file-img', 'file-other']
	obj = {}
	obj["content"] = content
	if msgType in acceptableMsgTypes:
		obj["type"] = msgType
	if attachment != None:
		obj["attachment"] = attachment
	return obj

class archiveCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	@commands.guild_only()
	async def archive(self, ctx, category):
		
		#print("[JOB START]: MERGING" + category.upper())
		categoryObject = discord.utils.get(ctx.guild.channels, name=str(category.lower()))
		categoryObject.channels

		embed = betterEmbeds(str(category))
		if discord.utils.get(ctx.guild.channels, name=str(category.lower()) + "-archive") is None:
			archive_channel = await ctx.guild.create_text_channel(category.lower() + "-archive",category=discord.utils.get(ctx.guild.categories, name="ARCHIVE"))
			await embed.add_destination(archive_channel)
			for textChannel in categoryObject.channels:
				if str(textChannel.type) == "text":
					#print(str(textChannel.name))
					messages = await textChannel.history().flatten()
					msgObject = processMessages(messages).getMessages()
					for m in msgObject:
						if m['type'] == "codeblock":
							await splitCodeMessage(m, textChannel, embed)
						elif m['type'] == "text":
							await splitTextMessage(m, textChannel, embed)
						elif m['type'] == "file-img":
							#await embed.add_field(str(textChannel.name), "![{}]".format(m['attachment']))
							await embed.add_image(str(textChannel.name), m['attachment'])
						elif m['type'] == "file-other":
							await embed.add_field("ATTACHMENT: ", "*{}*".format(m['attachment']))
			if embed.length > 0:
				await embed.send_message()
		else:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_ALREADY_MERGED")
	pass

def setup(bot):
	bot.add_cog(archiveCog(bot))