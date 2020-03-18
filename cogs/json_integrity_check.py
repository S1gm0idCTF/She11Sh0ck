import json

import discord
from discord.ext import tasks, commands

from errors import sendErrorMessage

class jsonIntegrity(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.integrityCheck.start() # pylint: disable= no-member

	@tasks.loop(seconds=10.0)
	async def integrityCheck(self):

		# Stuff this file needs to do:
		# ASSUME THE SERVER IS ALWAYS RIGHT
		# FOR EVERY SERVER:
		# 1. make sure for every category on the json, there is a matching category on the server
		#		if not, delete the category on the json
		# 2. make sure for every question on the server, there is a qustion in the json
		#		if not, add the question to the json
		# 3. make sure for every question in the json, there is a question on the server
		#		if not, delete the question on the json

		with open("server_config.json", "r") as f:
			settings = json.load(f)
		update = False

		for guild in self.bot.guilds:
			questions_to_pop = []
			cats_to_pop = []
			check1, check2, check3 = True, True, True
			for key in settings[str(guild.id)]:
				if key != "data":
					if discord.utils.get(guild.categories, name=key.lower()) is None:
						cats_to_pop.append(key)
						check1 = False #make sure for every category on the json there is one on the server
					else:
						category = discord.utils.get(guild.categories, name=key.lower())
						for key2 in settings[str(guild.id)][key]["questions"]:
							if key2 not in [channel.name for channel in category.channels]:
								# make sure for every question in category there's a question on the server
								questions_to_pop.append(key2) 
								check2 = False
						
						for channel in category.channels:
							if channel.name not in settings[str(guild.id)][key]["questions"].keys():
								settings[str(guild.id)][key]["questions"][channel.name] = False
								check3 = False

			for channel in questions_to_pop:
				settings[str(guild.id)][key]["questions"].pop(channel)
			
			for cat in cats_to_pop:
				settings[str(guild.id)].pop(cat)

			if not check1 or not check2 or not check3:
				print(check1, check2, check3,)
				print("things were fucked but are getting fixed now :D")
				update = True

		if update:		
			with open("server_config.json", "w") as f:
				json.dump(settings, f, indent=4)
		else:
			print("integrity check passed")
				
def setup(bot):
	bot.add_cog(jsonIntegrity(bot))
