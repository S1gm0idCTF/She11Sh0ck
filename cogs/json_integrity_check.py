import json

import discord
from discord.ext import tasks, commands

from errors import sendErrorMessage

class jsonIntegrity(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# self.integrityCheck.start()

	#@tasks.loop(seconds=1.0)
	@commands.command()
	@commands.guild_only()
	async def integrityCheck(self, ctx):

		# Shit this file needs to do:
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
							if channel.name not in settings[str(guild.id)][key].keys():
								settings[str(guild.id)][key]["questions"][channel.name] = False
								check3 = False
			print(cats_to_pop)
			print(questions_to_pop)
			for channel in questions_to_pop:
				settings[str(guild.id)][key]["questions"].pop(channel)
			
			for cat in cats_to_pop:
				settings[str(guild.id)].pop(cat)

			
		with open("server_config.json", "w") as f:
			json.dump(settings, f, indent=4)

		print("done")





				
def setup(bot):
	bot.add_cog(jsonIntegrity(bot))








# print("checking integrity")
		# with open("server_config.json", "r") as f:
		# 	config = json.load(f)
		
		
		# for guild in self.bot.guilds:
		# 	arr =[]
		# 	check1, check2 = True, True
		# 	for category in guild.categories: #for category on server
		# 		if category.name.lower() in config[str(guild.id)]: #if category is marked as a ctf
		# 			for key in config[str(guild.id)][category.name.lower()]["questions"]: # for question in that ctf
		# 				if key not in [textChannel.name for textChannel in category.channels]: #if questin exists on the json, but not the server we assume json is wrong
		# 					arr.append(key)
		# 					check2 = False
				
		# 		for key in arr:
		# 			config[str(guild.id)][category.name]["questions"].pop(key) # remove missing questions from json

		# 			for textChannel in category.channels: #for question in ctf
		# 				if textChannel.name not in config[str(guild.id)][category.name.lower()]["questions"]: #if question does not exist on the json
		# 					config[str(guild.id)][category.name.lower()]["questions"][textChannel.name] = False #we add the question to the json, assume it was wrong
		# 					check1 = False

		# 	for key in config[str(guild.id)]: # for CTF on json
		# 		print("key is:" + key)
		# 		print(discord.utils.get(guild.categories, name=key.lower()))
		# 		if discord.utils.get(guild.categories, name=key.lower()) is None:
		# 			print(config[str(guild.id)].pop(key))
			
		# 	if check1 and check2:
		# 		print("Things are ok on server: " + str(guild.id))
