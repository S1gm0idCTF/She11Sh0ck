import json
from errors import sendErrorMessage
import discord
from discord.ext import commands


class CTFSetup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.activeCTF = None

	async def isCTFActive(self, ctx):
		if not await self.getctf(ctx):
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_NOT_SET")	
			return False
		else:
			return True

	@commands.command()
	@commands.guild_only()
	async def currentctf(self, ctx):
		if await self.isCTFActive(ctx):
			await ctx.send("`{}`, is the selected CTF.".format(await self.getctf(ctx)))
		pass
	
	@commands.command()
	@commands.guild_only()
	async def setctf(self, ctx, ctfname):
		print("setting ctf: " + ctfname.lower())
		category = discord.utils.get(ctx.guild.categories, name=ctfname.lower())
		# print(category)
		if category != None:
			with open("server_config.json", "r") as f:
				settings = json.load(f)

			for key in settings[str(ctx.guild.id)]:
				settings[str(ctx.guild.id)][key]["active"] = False

			settings[str(ctx.guild.id)][category.name]["active"] = True

			with open("server_config.json", "w") as f:
				json.dump(settings, f, indent=4)

		else:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_NOT_FOUND")		
		pass

	async def getctf(self, ctx):
		with open("server_config.json", "r") as f:
			settings = json.load(f)
		for key in settings[str(ctx.guild.id)]:
			if settings[str(ctx.guild.id)][key]["active"] == True:
				return key

	@commands.command()
	@commands.guild_only()
	async def createctf(self, ctx, *ctfname):
		ctfname = "-".join(ctfname).lower()
		with open("server_config.json", "r") as f:
			settings = json.load(f)

		print("creating CTF: " + ctfname)
		if (
			not discord.utils.get(ctx.guild.categories, name=ctfname)
			and ctfname not in settings[str(ctx.guild.id)]
		):
			settings[str(ctx.guild.id)][ctfname] = {}
			await ctx.guild.create_category(ctfname)
			settings[str(ctx.guild.id)][ctfname]["questions"] = {}
			with open("server_config.json", "w") as f:
				json.dump(settings, f, indent=4)

			await self.setctf(ctx, ctfname)
		else:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_ALREADY_EXISTS")		
		pass

	@commands.command(name="addQ")
	@commands.guild_only()
	async def Q(self, ctx, *questionTitle):
		if await self.isCTFActive(ctx):
			print("adding question")
			with open("server_config.json", "r") as f:
				settings = json.load(f)
			questionTitle = "-".join(questionTitle).lower()
			if (
				questionTitle
				not in settings[str(ctx.guild.id)][await self.getctf(ctx)]["questions"]
			):
				category = discord.utils.get(
					ctx.guild.categories, name=await self.getctf(ctx)
				)
				await ctx.guild.create_text_channel(questionTitle, category=category)
				settings[str(ctx.guild.id)][await self.getctf(ctx)]["questions"][
					questionTitle
				] = False

				with open("server_config.json", "w") as f:
					json.dump(settings, f, indent=4)
			else:
				error = sendErrorMessage(ctx)
				await error.sendError("E_Q_ALREADY_EXISTS")

	@commands.command()
	@commands.guild_only()
	async def markSolved(self, ctx, Q):
		if await self.isCTFActive(ctx):
			with open("server_config.json", "r") as f:
				settings = json.load(f)

			if Q in settings[str(ctx.guild.id)][await self.getctf(ctx)]["questions"]:
				settings[str(ctx.guild.id)][await self.getctf(ctx)]["questions"][
					Q
				] = True

				with open("server_config.json", "w") as f:
					json.dump(settings, f, indent=4)
			else:
				error = sendErrorMessage(ctx)
				await error.sendError("E_Q_NOT_FOUND")	

	@commands.command()
	@commands.guild_only()
	async def ctfQs(self, ctx):
		if await self.isCTFActive(ctx):
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


def setup(bot):
	bot.add_cog(CTFSetup(bot))
