import sys
import traceback
import json

import discord
from discord.ext import commands
from errors import sendErrorMessage

try:
	f = open("keys.txt", "r")
	TOKEN = f.readline().strip()
except:
	raise ValueError("You need to supply a keys.txt file. Instructions can be found in the README.md file")


async def get_prefix(bot, message):
	"""A callable Prefix for our bot. This could be edited to allow per server prefixes."""
	
	# Notice how you can use spaces in prefixes. Try to keep them simple though.
	prefixes = ["!ctf "]

	if message.content.startswith(prefixes[0].replace(" ", "")):
		await message.delete(delay=500)

	# Check to see if we are outside of a guild. e.g DM's etc.
	# Only allow ? to be used in DMs
	if not message.guild:
		return "?"

	# If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
	print(message.id)
	return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = [
	"cogs.archive",
	"cogs.ctf_setup_commands",
	"cogs.ctf_utility_commands",
	"cogs.owner_commands",
	"cogs.json_integrity_check"
]

bot = commands.Bot(command_prefix=get_prefix,
                   description="The cog enabled rewrite")

if __name__ == "__main__":
	for extension in initial_extensions:
		bot.load_extension(extension)


@bot.event
async def on_ready():
	print(
		f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
	)

	# Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
	print(f"Successfully logged in and booted...!")
	try:
		with open("server_config.json", "r") as f:
			settings = json.load(f)
	except:
		raise ValueError("You need to create server_config.json file. Instructions can be found in the README.md file.")
	print(settings)

	for guild in bot.guilds:
		if str(guild.id) not in settings:
			settings[str(guild.id)] = {}

	with open("server_config.json", "w") as f:
		json.dump(settings, f, indent=4)


@bot.event
async def on_guild_join(guild):
	with open("server_config.json", "r") as f:
		settings = json.load(f)

	settings[str(guild.id)] = {}

	with open("server_config.json", "w") as f:
		json.dump(settings, f, indent=4)

# @bot.event
# async def on_command_error(ctx, errormsg):
# 		"""The event triggered when an error is raised while invoking a command.
# 			ctx   : Context
# 			error : Exception"""
# 		error = sendErrorMessage(ctx)
# 		await error.sendError(errormsg)

bot.run(TOKEN, bot=True)