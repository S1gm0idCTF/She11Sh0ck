import asyncio
import json
import sys
import traceback

import discord
from discord.ext import commands, tasks

import sql
from creds import getDiscordAPIKeys
from errors import sendErrorMessage

try:
	TOKEN = getDiscordAPIKeys()
except:
	raise ValueError(
		"You need to supply a creds.json file. Instructions can be found in the README.md file"
	)


async def get_prefix(bot, message):
	"""A callable Prefix for our bot. This could be edited to allow per server prefixes."""

	# Notice how you can use spaces in prefixes. Try to keep them simple though.
	prefixes = ["!ctf ", "?"]

	# If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
	return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = [
	"cogs.archive",
	"cogs.ctf_setup_commands",
	"cogs.ctf_utility_commands",
	"cogs.owner_commands",
	"cogs.ctftime_stats",
	"cogs.solve_check",
	"cogs.helpCog",
	"cogs.misc_commands",
]

bot = commands.Bot(command_prefix=get_prefix, description="The cog enabled rewrite")


@bot.event
async def on_ready():
	print(
		f"\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
	)

	# Changes our bots Playing Status. type=1(streaming) for a standard game you could remove type and url.
	print(f"Ready to Party.")
	for guild in bot.guilds:
		guild_in_db = await sql.db.getGuildByID(guild.id)
		if guild_in_db == None:
			print("GUILD ERROR: " + str(guild.id))
			await sql.db.addGuild(guild.id, guild.name)
			print("GUILD " + str(guild.id) + " added to DB")


@bot.event
async def on_guild_join(guild):
	await sql.db.addGuild(guild.id, guild.name)


@bot.event
async def on_command_error(ctx, errormsg):
	"""The event triggered when an error is raised while invoking a command.
	ctx   : Context
	error : Exception"""
	error = sendErrorMessage(ctx)
	print(errormsg)
	await error.sendError("E_GENERIC")


if __name__ == "__main__":
	sql.init()
	async_loop = asyncio.get_event_loop()
	async_loop.create_task(sql.db.createPool(async_loop))
	print("SQL DB STARTED")

	bot.remove_command("help")
	for extension in initial_extensions:
		bot.load_extension(extension)

	bot.run(TOKEN, bot=True)
