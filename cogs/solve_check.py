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

	@tasks.loop(seconds=1.0)
	async def solveCheck(self):
		for guild in self.bot.guilds:
			ctfs = await sql.db.getAllGuildCTFIDs(guild.id)
			print(ctfs)
			
def setup(bot):
	bot.add_cog(solveChecker(bot))