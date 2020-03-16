import json

import discord
from discord.ext import commands

class CTFSetup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.activeCTF = None

	@commands.command()
	@commands.guild_only()
	async def currentCTF(self, ctx):
		if await self.getCTF(ctx):
			await ctx.send("`{}`, is the selected CTF.".format(await self.getCTF(ctx)))
		pass

	@commands.command()
	@commands.guild_only()
	async def setCTF(self, ctx, ctfname):
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
				json.dump(settings, f, indent = 4)
			
		else:
			await ctx.send("That ctf doesn't exist :(")
		pass

	async def getCTF(self, ctx):
		with open("server_config.json", "r") as f:
				settings = json.load(f)
		for key in settings[str(ctx.guild.id)]:
			if settings[str(ctx.guild.id)][key]["active"] == True:
				return key

	@commands.command()
	@commands.guild_only()
	async def createCTF(self, ctx, *ctfname):
		ctfname = "-".join(ctfname).lower()
		with open("server_config.json", "r") as f:
				settings = json.load(f)
				
		print("creating CTF: " + ctfname)
		if not discord.utils.get(ctx.guild.categories, name=ctfname) and ctfname not in settings[str(ctx.guild.id)]:
			settings[str(ctx.guild.id)][ctfname] = {}
			await ctx.guild.create_category(ctfname)
			settings[str(ctx.guild.id)][ctfname]["questions"] = {}
			with open("server_config.json", "w") as f:
				json.dump(settings, f, indent = 4)

			await self.setCTF(ctx, ctfname)
		else:
			await ctx.send("A CTF with this name already exists")
		pass

	@commands.command(name="addQ")
	@commands.guild_only()
	async def Q(self, ctx, *questionTitle):
		print("adding question")
		with open("server_config.json", "r") as f:
			settings = json.load(f)
		questionTitle = "-".join(questionTitle).lower()
		if questionTitle not in settings[str(ctx.guild.id)][await self.getCTF(ctx)]["questions"]:
			category = discord.utils.get(
				ctx.guild.categories, name= await self.getCTF(ctx)
			)
			await ctx.guild.create_text_channel(questionTitle, category=category)

			
			for textChannel in category.channels:
				if textChannel.name not in settings[str(ctx.guild.id)][await self.getCTF(ctx)]["questions"]:
					solveCheck = await textChannel.history().flatten()
					solveCheck = [x.content for x in solveCheck]
					print(solveCheck)
					if "SOLVED" in solveCheck:
						settings[str(ctx.guild.id)][await self.getCTF(ctx)]["questions"][questionTitle] = True
					else:
						settings[str(ctx.guild.id)][await self.getCTF(ctx)]["questions"][questionTitle] = False
			with open("server_config.json", "w") as f:
				json.dump(settings, f, indent = 4)
		else:
			await ctx.send("A question with that name already exists")
			# print(self.activeCTF.getQs())
		pass

	@commands.command()
	@commands.guild_only()
	async def markSolved(self, ctx, Q):
		with open("server_config.json", "r") as f:
				settings = json.load(f)

		if Q in settings[str(ctx.guild.id)][await self.getCTF(ctx)]["questions"]:
			settings[str(ctx.guild.id)][await self.getCTF(ctx)]["questions"][Q] = True
			
			with open("server_config.json", "w") as f:
				json.dump(settings, f, indent = 4)
		else:
			await ctx.send("This question does not exist")
		pass

	@commands.command()
	@commands.guild_only()
	async def ctfQs(self, ctx):
		await ctx.send("The current Questions are: ")
		send = ""
		with open("server_config.json", "r") as f:
				settings = json.load(f)

		for key in settings[str(ctx.guild.id)][await self.getCTF(ctx)]["questions"]:
			if settings[str(ctx.guild.id)][await self.getCTF(ctx)]["questions"][key] == True:
				send += key + " | " + "SOLVED!!!\n"
			else:
				send += key + " | " + "unsolved\n"

		await ctx.send(send)


def setup(bot):
	bot.add_cog(CTFSetup(bot))
