import json

import discord
from discord.ext import tasks, commands

from errors import sendErrorMessage

class jsonIntegrity(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.integrityCheck.start() # pylint: disable= no-member

	@tasks.loop(seconds=1200.0) # runs the integrity check every 20 minutes
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
								# make sure for every question in json category there's a question on the server
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
				print("integrity check failed")
				print("[1] Every CTF on the JSON has a corresponding category on the server: ", check1)
				if not check1:
					print("	Deleting the missing CTF from the json")
				print("[2] Every question on the json has a corresponding text channel on the server: ", check2)
				if not check2:
					print("	Deleting the missing question from the json")
				print("[3] Every question on the server has a corresponding question in the json: ", check3)
				if not check3:
					print("	Adding an unsolved question with the correct name to the json")
				update = True

		if update:		
			with open("server_config.json", "w") as f:
				json.dump(settings, f, indent=4)
		else:
			print("integrity check passed")
				
def setup(bot):
	bot.add_cog(jsonIntegrity(bot))
