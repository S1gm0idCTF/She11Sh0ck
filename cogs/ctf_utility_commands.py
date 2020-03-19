import discord
from discord.ext import commands


from etc.encryptions import *

from etc.pipes import ProcessPipe

pipe = " | "

class CTFUtility(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
##########################################################
	@commands.command()
	@commands.guild_only()
	async def count(self, ctx, *s):
		s = ' '.join(s)
		await ctx.send(str(len(s)) + " characters long.")
##########################################################
	@commands.command()
	@commands.guild_only()
	async def b64(self, ctx, f, *s):
		s = ' '.join(s)
		if pipe in s:
			pp = ProcessPipe("b64 {} {}".format(f,s))
			output = pp.getString()
		else:
			output = do_b64(f,s)
		await ctx.send(output)
	pass
##########################################################
	@commands.command()
	@commands.guild_only()
	async def b32(self, ctx, f, *s):
		s = ' '.join(s)
		if pipe in s:
			pp = ProcessPipe("b32 {} {}".format(f,s))
			output = pp.getString()
		else:
			output = do_b32(f,s)
		await ctx.send(output)
	pass
##########################################################
	@commands.command()
	@commands.guild_only()
	async def hex(self, ctx, f, *s):
		s = ' '.join(s)
		if pipe in s:
			pp = ProcessPipe("hex {} {}".format(f,s))
			output = pp.getString()
		else:
			output = do_hex(f,s)
		await ctx.send(output)
	pass
##########################################################
	@commands.command()
	@commands.guild_only()
	async def b16(self, ctx, f, *s):
		s = ' '.join(s)
		if pipe in s:
			pp = ProcessPipe("b16 {} {}".format(f,s))
			output = pp.getString()
		else:
			output = do_b16(f,s)
		await ctx.send(output)
	pass
##########################################################
	@commands.command()
	@commands.guild_only()
	async def binary(self, ctx, f, *s):
		s = ' '.join(s)
		if pipe in s:
			pp = ProcessPipe("binary {} {}".format(f,s))
			output = pp.getString()
		else:
			output = do_binary(f,s)
		await ctx.send(output)
	pass
##########################################################
def setup(bot):
	bot.add_cog(CTFUtility(bot))


