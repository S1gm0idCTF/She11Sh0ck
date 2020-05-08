import json

import discord
from discord.ext import tasks, commands

import sql
from errors import sendErrorMessage
from etc.betterEmbeds import sendEmbed

class solveChecker(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.solveCheck.start()

	@tasks.loop(seconds=600.0)
	async def solveCheck(self):
		for guild in self.bot.guilds:
			ctfs = await sql.db.getAllGuildCTFDATA(guild.id)
			for ctf in ctfs:
				flagFormat = await sql.db.getFlagFormat(ctf[0])
				flagFormat = flagFormat[0]
				print(flagFormat)
				category = discord.utils.get(guild.categories, name=ctf[1].lower())
				for channel in category.channels:
					messages = await channel.history(limit=20).flatten()
					for message in messages:
						if flagFormat in message.content and flagFormat != "PLACEHOLDER_UNTIL_UPDATE_FLAG" and "?" + flagFormat not in message.content:
							
							await sql.db.setSolved(channel.name, ctf[0])

def setup(bot):
	bot.add_cog(solveChecker(bot))