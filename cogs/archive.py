import discord
from discord.ext import commands
from datetime import datetime
async def splitTextMessage(message, textChannel,embed):
	i = -1
	message = message['content']
	while len(message) > 997:
		i = message[0:995].rfind('\n')
		if i == -1:
			i = message[0:995].rfind(' ')
		if i == -1:
			i = 950
		print("SENDING: {}".format(message[0:i]))
		await embed.add_field(str(textChannel.name), message[0:i])					
		message = message[i:]
	await embed.add_field(str(textChannel.name), message)

async def splitCodeMessage(message, textChannel, embed):
	i = -1
	message = message['content']
	while len(message) > 997:
		i = message[0:995].rfind('\n')
		if i == -1:
			i = message[0:995].rfind(' ')
		if i == -1:
			i = 950
		print("SENDING: {}".format(message[0:i]))
		await embed.add_field(str(textChannel.name), "```{}```".format(message[0:i]))
		message = message[i:]
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
            if message.count("`") % 2 == 0 and message.count("`") > 0:
                while "``" in message:
                    message = message.replace("``", "`")
                while "```" in message:
                    message = message.replace("```", "`")
                codeblockIndex = [pos+1 for pos, char in enumerate(message) if char == '`']
                if codeblockIndex[0] != 0:
                    #if the there's whitespace between first message, and `
                    formattedMessages.append(embedsObj(message[0:(codeblockIndex[0]-1)],"text"))
                    print("t:" + str(message[0:(codeblockIndex[0]-1)]))
                while len(codeblockIndex) > 1:
                    substr = message[codeblockIndex[0]:codeblockIndex[1]-1]
                    formattedMessages.append(embedsObj(substr,"codeblock"))
                    print(">>" + substr)
                    if len(codeblockIndex) > 2:
                        if message[codeblockIndex[1]:codeblockIndex[2]-1] != "":
                            formattedMessages.append(embedsObj(substr,"text"))
                            print("t:" + message[codeblockIndex[1]:codeblockIndex[2]-1])
                    codeblockIndex = codeblockIndex[2:]
            else:
                formattedMessages.append(embedsObj(message, "text"))
            if msg.attachments != []:
                for attchmnt in msg.attachments:
                    formattedMessages.append(embedsObj(".", "file-img", attchmnt.url))
        return formattedMessages

class betterEmbeds():
	def __init__(self, category):
		self.embed = discord.Embed(title="# {}".format(str(category)),description="### Created: {}".format(str(datetime.now())),color=0xFF0000)
		self.destination = ''
		self.length = 0 
		self.objectCount = 0 

	async def test_embed(self, bodyLength):
		if (self.length + bodyLength >= 6000) or (self.objectCount + 1 >= 12): 
			return False
		else:
			return True

	async def reInitialize(self,textChannelName):
		self.embed = discord.Embed(title="# {}".format(str(textChannelName)),description="### Created: {}".format(str(datetime.now())),color=0xFF0000)
		self.length = 0
		self.objectCount = 0

	async def add_field(self, textChannelName, body):
		if len(body) < 3:
			return
		print(self.objectCount)
		if not await self.test_embed(len(body)):
			print("FAILED")
			#Failed Constraint Check
			if self.destination == '':
				print("I don't know where to send this :/")
			else:
				await self.send_message()
				await self.reInitialize(str(textChannelName))
		self.length = self.length + len(body)
		self.objectCount = self.objectCount + 1 
		self.embed.add_field(name=str("### " + textChannelName),value=body + "\n", inline=False)

	async def add_destination(self,destination):
		print("Destination SET: " + str(destination))
		self.destination = destination

	async def send_message(self):
		await self.destination.send(embed=self.embed)

class archiveCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	async def archive(self, ctx, category):
	# merging doesn't delete the originals in case of an accidental merge
		print("[JOB START]: MERGING" + category.upper())
		categoryObject = discord.utils.get(ctx.guild.channels, name=str(category.lower()))
		
		embed = betterEmbeds(str(category))

		if discord.utils.get(ctx.guild.channels, name=str(category.lower()) + "-archive") is None:
			await ctx.guild.create_text_channel(category + "-archive",category=discord.utils.get(ctx.guild.categories, name="ARCHIVE"))
			archive_channel =  self.bot.get_channel(discord.utils.get(ctx.guild.channels, name=str(category.lower()) + "-archive").id)    
			await embed.add_destination(archive_channel)
			for textChannel in categoryObject.channels:
				if str(textChannel.type) == "text":
					print(str(textChannel.name))
					messages = await textChannel.history().flatten()
					msgObject = processMessages(messages).getMessages()
					for m in msgObject:
						if m['type'] == "codeblock":
							await splitCodeMessage(m, textChannel, embed)
						elif m['type'] == "text":
							await splitTextMessage(m, textChannel, embed)
						elif m['type'] == "file-img":
							await embed.add_field(str(textChannel.name), f"![{m['attachment']}]")
			if embed.length > 0:
				await embed.send_message()
		else:
			await ctx.send("This CTF has already been merged or something has gone very, very wrong :(")
		pass

	@commands.command()
	@commands.guild_only()
	async def archive(self, ctx, category):
		# merging doesn't delete the originals in case of an accidental merge
		print("merging category: " + category)
		categoryObject = discord.utils.get(ctx.guild.channels, name=category)
		embed = discord.Embed(
			title="# {}".format(str(category)),
			description="### Created: {}".format(str(datetime.now())),
			color=0xFF0000,
		)
		exportWriteup = ""
		if discord.utils.get(ctx.guild.channels, name=category + "-archive") is None:
			await ctx.guild.create_text_channel(
				category + "-archive",
				category=discord.utils.get(ctx.guild.categories, name="ARCHIVE"),
			)
			archive_channel = self.bot.get_channel(
				discord.utils.get(ctx.guild.channels, name=category + "-archive").id
			)
			i = 0
			for textChannel in categoryObject.channels:
				if i > 5:
					await archive_channel.send(embed=embed)
					embed = discord.Embed(
						title="# {}".format(str(category)),
						description="## Created: {}".format(str(datetime.now())),
						color=0xFF0000,
					)
					i = 0
				if str(textChannel.type) == "text":
					print(str(textChannel.name))
					channelWriteup = ""
					messages = await textChannel.history().flatten()
					m = [x.content for x in messages][::-1]  # reverse messages

					for body in m:
						channelWriteup = channelWriteup + " - " + body + "\n"
					embed.add_field(
						name=str("### " + textChannel.name),
						value=channelWriteup + "\n",
						inline=False,
					)
				i = i + 1
			if i != 1:
				await archive_channel.send(embed=embed)
		else:
			await ctx.send(
				"This CTF has already been merged or something has gone very, very wrong :("
			)
		exportWriteup = ""
		pass


def setup(bot):
    bot.add_cog(archiveCog(bot))