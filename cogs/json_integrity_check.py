import json

import discord
from discord.ext import tasks, commands

from errors import sendErrorMessage

class jsonIntegrity(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.integrityCheck.start()

	@tasks.loop(seconds=1.0)
	async def integrityCheck(self):

		# this whole function is fucked and needs a rewrite
		
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

			
				
		# with open("server_config.json", "w") as f:
		# 	json.dump(config, f, indent=4)

		

				
def setup(bot):
	bot.add_cog(jsonIntegrity(bot))