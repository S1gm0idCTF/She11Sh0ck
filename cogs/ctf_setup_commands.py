import json

import discord
from discord.ext import commands


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


class CTFSetup(commands.Cog):
	def __init__(self, bot, activeCTF):
		self.bot = bot
		self.activeCTF = activeCTF

	async def isCTFActive(self, ctx):
		if self.activeCTF.getCTF() == "":
			await ctx.send(
				"Please run `!ctf setCTF [ctfname]` or `!ctf createCTF[ctfname]`first."
			)
			return False
		else:
			return True

	@commands.command()
	@commands.guild_only()
	async def currentCTF(self, ctx):
		if await self.isCTFActive(ctx):
			await ctx.send("`{}`, is the selected CTF.".format(self.activeCTF.getCTF()))
		pass

	@commands.command()
	@commands.guild_only()
	async def setCTF(self, ctx, ctfname):
		print("setting ctf: " + ctfname.lower())
		category = discord.utils.get(ctx.guild.categories, name=ctfname.lower())
		# print(category)
		if category != None:
			self.activeCTF.setCTF(ctfname.lower())
			self.activeCTF.clearData()
			await self.updateQs(ctx)
		else:
			await ctx.send("That ctf doesn't exist :(")
		pass

	@commands.command()
	@commands.guild_only()
	async def createCTF(self, ctx, *ctfname):
		ctfname = "-".join(ctfname).lower()
		print("creating CTF: " + ctfname)
		if not discord.utils.get(ctx.guild.categories, name=ctfname):
			await ctx.guild.create_category(ctfname)
			self.activeCTF.setCTF(ctfname)
		else:
			await ctx.send("A CTF with this name already exists")
		pass

	@commands.command(name="addQ")
	@commands.guild_only()
	async def Q(self, ctx, *questionTitle):
		print("adding question")
		if self.isCTFActive(ctx):
			questionTitle = "-".join(questionTitle).lower()
			category = discord.utils.get(
				ctx.guild.categories, name=self.activeCTF.getCTF()
			)
			await ctx.guild.create_text_channel(questionTitle, category=category)
			for textChannel in category.channels:
				if textChannel.name not in self.activeCTF.getQs():
					solveCheck = await textChannel.history().flatten()
					solveCheck = [x.content for x in solveCheck]
					print(solveCheck)
					if "SOLVED" in solveCheck:
						self.activeCTF.addQ(textChannel.name, True)
					else:
						self.activeCTF.addQ(textChannel.name, False)
			print(self.activeCTF.getQs())
		pass

	@commands.command()
	@commands.guild_only()
	async def updateQs(self, ctx):
		category = discord.utils.get(ctx.guild.categories, name=self.activeCTF.getCTF())
		for textChannel in category.channels:
			solveCheck = await textChannel.history().flatten()
			solveCheck = [x.content for x in solveCheck]
			if textChannel.name not in self.activeCTF.getQs().keys():
				if "SOLVED" in solveCheck:
					self.activeCTF.addQ(textChannel.name, True)
				else:
					self.activeCTF.addQ(textChannel.name, False)
			else:
				print(textChannel.name)
				print(self.activeCTF.getQs()[textChannel.name])
				if (
					"SOLVED" in solveCheck
					or self.activeCTF.getQs()[textChannel.name] == True
				):
					self.activeCTF.updateQ(textChannel.name, True)
				else:
					self.activeCTF.updateQ(textChannel.name, False)

	@commands.command()
	@commands.guild_only()
	async def markSolved(self, ctx, Q):
		category = discord.utils.get(ctx.guild.categories, name=self.activeCTF.getCTF())
		if Q in [channel.name for channel in category.channels]:
			self.activeCTF.updateQ(Q, True)
		else:
			await ctx.send("This question does not exist")
		pass

	@commands.command()
	@commands.guild_only()
	async def ctfQs(self, ctx):
		if await self.getctf(ctx):
			await ctx.send("The current Questions are: ")
			send = ""
			with open("server_config.json", "r") as f:
				settings = json.load(f)
			i = 1
			for key in settings[str(ctx.guild.id)][await self.getctf(ctx)]["questions"]:
				if (
					settings[str(ctx.guild.id)][await self.getctf(ctx)]["questions"][
						key
					]
					== True
				):
					send += "[{}] ".format(i) + "~~"  + key + "~~\n"
				else:
					send += "[{}] ".format(i) + key + "\n"
				i = i + 1 
			await ctx.send(send)
		else:
			await ctx.send(
				"There is no CTF currently selected. Please select one with `!ctf setctf <name>` or create one with `!ctf createctf <name>`"
			)



def setup(bot):
	bot.add_cog(CTFSetup(bot, CTF()))
