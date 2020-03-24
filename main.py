import sys
import traceback
import json
import discord
import asyncio
from creds import getDiscordAPIKeys
from discord.ext import tasks, commands
from errors import sendErrorMessage
#--------------------------------------
import sql
from dbhandler import database
sql.init()
sql.db = database()


def start(loop):
  
  loop.create_task(sql.db.createPool(loop))
  
loop = asyncio.get_event_loop()
start(loop)


try:
	TOKEN = getDiscordAPIKeys()
except:
	raise ValueError("You need to supply a keys.txt file. Instructions can be found in the README.md file")


async def get_prefix(bot, message):
	"""A callable Prefix for our bot. This could be edited to allow per server prefixes."""
	
	# Notice how you can use spaces in prefixes. Try to keep them simple though.
	prefixes = ["!ctf "]

	# Check to see if we are outside of a guild. e.g DM's etc.
	# Only allow ? to be used in DMs
	if not message.guild:
		return "?"

	# If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
	return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = [
	"cogs.archive",
	"cogs.ctf_setup_commands",
	"cogs.ctf_utility_commands",
	"cogs.owner_commands",
	"cogs.json_integrity_check",
	"cogs.ctftime_stats",
	"cogs.helpCog"
]

bot = commands.Bot(command_prefix=get_prefix,
                   description="The cog enabled rewrite")

if __name__ == "__main__":
	bot.remove_command("help")
	for extension in initial_extensions:
		bot.load_extension(extension)


@bot.event
async def on_ready():
	print(
		f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
	)
	
	# Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
	print(f"Ready to Party.")
	
@bot.event
async def on_guild_join(guild):
	await sql.db.addGuild(guild.id,guild.name)

@bot.event
async def on_command_error(ctx, errormsg):
	"""The event triggered when an error is raised while invoking a command.
	ctx   : Context
	error : Exception"""
	error = sendErrorMessage(ctx)
	await error.sendError(errormsg)

bot.run(TOKEN, bot=True)