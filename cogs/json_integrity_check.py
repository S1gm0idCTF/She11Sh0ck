import json

import discord
from discord.ext import commands

from errors import sendErrorMessage

class jsonIntegrity(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	async def integrityCheck(self, ctx, category):
		with open("server_config.json", "r") as f:
			check1, check2 = True, True
			config = json.load(f)
			print(category)
			category = discord.utils.get(ctx.guild.categories, name=str(category.lower()))
		
		for textChannel in category.channels:
			if textChannel.name not in config[str(ctx.guild.id)][category.name]["questions"]:
				config[str(ctx.guild.id)][category.name]["questions"][textChannel.name] = False
				check1 = False

		arr =[]
		#avoids changing size of json mid for loop
		for key in config[str(ctx.guild.id)][category.name]["questions"]:
			if key not in [textChannel.name for textChannel in category.channels]:
				arr.append(key)
				check2 = False
		
		for key in arr:
			config[str(ctx.guild.id)][category.name]["questions"].pop(key)
		
		with open("server_config.json", "w") as f:
					json.dump(config, f, indent=4)

		if check1 and check2:
			await ctx.send("All be good")

		print(check1)
		print(check2)
def setup(bot):
	bot.add_cog(jsonIntegrity(bot))