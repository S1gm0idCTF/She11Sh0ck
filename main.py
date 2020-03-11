import base64
import datetime
import string
import time

import discord
import numpy
import pwn
from discord.ext import commands
import datetime

f = open("keys.txt", "r")
TOKEN = f.readline().strip()
serverID = int(f.readline().strip())

###############################################################################################
#####################################  VARIABLES  #############################################
###############################################################################################

bot = commands.Bot(command_prefix="!")


class CTF:
	def __init__(self):
		self.activeCTF = ""
		self.QDict = {}

	def setCTF(self, ctfname):
		self.activeCTF = ctfname

	def getCTF(self):
		return self.activeCTF

	def addQ(self, QName, solved):
		self.QDict.update({QName: solved})

	def updateQ(self, QName, solved):
		self.QDict[QName] = solved

	def getQs(self):
		return self.QDict

	def clearData(self):
		self.QDict = {}


activeCTF = CTF()

###############################################################################################
#####################################  EVENTS  ################################################
###############################################################################################


@bot.event
async def on_ready():
	global activeCTF
	print("Logged on as")
	print(bot.user.name)
	print(bot.user.id)
	print("--------")


@bot.event
async def on_message(message):
	# print(
	# 	"Message from {0.author}: {0.content} in channel: {0.channel}".format(message)
	# )
	await bot.process_commands(message)


###############################################################################################
#####################################  COMMANDS  ##############################################
###############################################################################################
@bot.command()
async def currentctf(ctx):
	if activeCTF.getCTF() == "":
		await ctx.send("Please run `!setctf [ctfname]` or `!createctf [ctfname]`first.")
	else:
		await ctx.send("`{}`, is the selected CTF.".format(activeCTF.getCTF()))
	pass


@bot.command()
async def setctf(ctx, ctfname):
	print("setting ctf: " + ctfname.lower())
	category = discord.utils.get(ctx.guild.categories, name=ctfname.lower())
	# print(category)
	if category != None:
		activeCTF.setCTF(ctfname.lower())
		activeCTF.clearData()
		await updateQs(ctx)
	else:
		await ctx.send("That ctf doesn't exist :(")
	pass


@bot.command()
async def createctf(ctx, *ctfname):
	ctfname = "-".join(ctfname).lower()
	print("creating CTF: " + ctfname)
	if not discord.utils.get(ctx.guild.categories, name=ctfname):
		await ctx.guild.create_category(ctfname)
		activeCTF.setCTF(ctfname)
	else:
		await ctx.send("A CTF with this name already exists")
	pass


@bot.command()
async def Q(ctx, *questionTitle):
	print("adding question")
	if activeCTF.getCTF() == "":
		await ctx.send("Please run `!setctf [ctfname]` or `!ctf [ctfname]`first.")
	else:
		questionTitle = "-".join(questionTitle).lower()
		category = discord.utils.get(ctx.guild.categories, name=activeCTF.getCTF())
		await ctx.guild.create_text_channel(questionTitle, category=category)
		for textChannel in category.channels:
			if textChannel.name not in activeCTF.getQs():
				solveCheck = await textChannel.history().flatten()
				solveCheck = [x.content for x in solveCheck]
				print(solveCheck)
				if "SOLVED" in solveCheck:
					activeCTF.addQ(textChannel.name, True)
				else:
					activeCTF.addQ(textChannel.name, False)
		print(activeCTF.getQs())
	pass


@bot.command()
async def updateQs(ctx):
	category = discord.utils.get(ctx.guild.categories, name=activeCTF.getCTF())
	for textChannel in category.channels:
		solveCheck = await textChannel.history().flatten()
		solveCheck = [x.content for x in solveCheck]
		print(solveCheck)
		if textChannel.name not in activeCTF.getQs().keys():
			if "SOLVED" in solveCheck:
				activeCTF.addQ(textChannel.name, True)
			else:
				activeCTF.addQ(textChannel.name, False)
		else:
			if "SOLVED" in solveCheck:
				activeCTF.updateQ(textChannel.name, True)
			else:
				activeCTF.updateQ(textChannel.name, False)
	print(activeCTF.getQs())


@bot.command()
async def ctfQs(ctx):
	await ctx.send("The current Questions are: ")
	await updateQs(ctx)
	send = ""
	for key in activeCTF.QDict:
		if activeCTF.QDict[key] == True:
			send += key + " | " + "SOLVED!!!\n"
		else:
			send += key + " | " + "unsolved\n"

	await ctx.send(send)


@bot.command()
async def merge(ctx, category):
	# merging doesn't delete the originals in case of an accidental merge
	print("merging category: " + category)
	categoryObject = discord.utils.get(ctx.guild.channels, name=category)
	embed = discord.Embed(
		title="# {}".format(str(category)),
		description="### Created: {}".format(str(datetime.datetime.now())),
		color=0xFF0000,
	)
	exportWriteup = ""
	if discord.utils.get(ctx.guild.channels, name=category + "-archive") is None:
		await ctx.guild.create_text_channel(
			category + "-archive",
			category=discord.utils.get(ctx.guild.categories, name="ARCHIVE"),
		)
		archive_channel = bot.get_channel(
			discord.utils.get(ctx.guild.channels, name=category + "-archive").id
		)
		i = 0
		for textChannel in categoryObject.channels:
			if i > 5:
				await archive_channel.send(embed=embed)
				embed = discord.Embed(
					title="# {}".format(str(category)),
					description="## Created: {}".format(str(datetime.datetime.now())),
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


# Actual CTF commands


@bot.command()
async def b64Decode(ctx, string):
	await ctx.send(base64.b64decode(string).decode("utf-8"))


@bot.command()
async def b64Encode(ctx, string):
	await ctx.send(base64.b64encode(string.encode()).decode("utf-8"))


@bot.command()
async def binaryDecode(ctx, binary_string):
	binary_string = binary_string.replace(" ", "")
	print(binary_string)
	string = "".join(
		chr(int(binary_string[i * 8 : i * 8 + 8], 2))
		for i in range(len(binary_string) // 8)
	)
	await ctx.send(string)


###############################################################################################

bot.run(TOKEN)
