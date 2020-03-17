import sys
import traceback
import json

import discord
from discord.ext import commands
from errors import sendErrorMessage

f = open("keys.txt", "r")
TOKEN = f.readline().strip()
serverID = int(f.readline().strip())

def get_prefix(bot, message):
	"""A callable Prefix for our bot. This could be edited to allow per server prefixes."""

	# Notice how you can use spaces in prefixes. Try to keep them simple though.
	prefixes = ["!ctf "]

	# Check to see if we are outside of a guild. e.g DM's etc.
	if not message.guild:
		# Only allow ? to be used in DMs
		return "?"

	# If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
	
	return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = [
	"cogs.archive",
	"cogs.ctf_setup_commands",
	"cogs.ctf_utility_commands",
	"cogs.owner_commands",
	"cogs.error"
]

bot = commands.Bot(command_prefix=get_prefix, description="The cog enabled rewrite")

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

bot.run(TOKEN, bot=True)
