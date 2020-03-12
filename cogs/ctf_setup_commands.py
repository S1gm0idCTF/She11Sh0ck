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


class ctfSetup(commands.Cog):
	def __init__(self, bot, activeCTF):
		self.bot = bot
		self.activeCTF = activeCTF

	@commands.command()
	@commands.guild_only()
	async def currentctf(self, ctx):
		if self.activeCTF.getCTF() == "":
			await ctx.send(
				"Please run `!setctf [ctfname]` or `!createctf [ctfname]`first."
			)
		else:
			await ctx.send("`{}`, is the selected CTF.".format(self.activeCTF.getCTF()))
		pass

	@commands.command()
	@commands.guild_only()
	async def setctf(self, ctx, ctfname):
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
	async def createctf(self, ctx, *ctfname):
		ctfname = "-".join(ctfname).lower()
		print("creating CTF: " + ctfname)
		if not discord.utils.get(ctx.guild.categories, name=ctfname):
			await ctx.guild.create_category(ctfname)
			self.activeCTF.setCTF(ctfname)
		else:
			await ctx.send("A CTF with this name already exists")
		pass

	@commands.command()
	@commands.guild_only()
	async def Q(self, ctx, *questionTitle):
		print("adding question")
		if self.activeCTF.getCTF() == "":
			await ctx.send("Please run `!setctf [ctfname]` or `!ctf [ctfname]`first.")
		else:
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
				if "SOLVED" in solveCheck:
					self.activeCTF.updateQ(textChannel.name, True)
				else:
					self.activeCTF.updateQ(textChannel.name, False)

	@commands.command()
	@commands.guild_only()
	async def ctfQs(self, ctx):
		await ctx.send("The current Questions are: ")
		await self.updateQs(ctx)
		send = ""
		for key in self.activeCTF.QDict:
			if self.activeCTF.QDict[key] == True:
				send += key + " | " + "SOLVED!!!\n"
			else:
				send += key + " | " + "unsolved\n"

		await ctx.send(send)


def setup(bot):
	bot.add_cog(ctfSetup(bot, CTF()))

