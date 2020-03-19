import discord
import urllib.parse
from discord.ext import commands
from etc.encryptions import *
from etc.pipes import ProcessPipe

pipe = " | "

class CTFUtility(commands.Cog):
##########################################################
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	@commands.guild_only()
	async def exiftool(self,ctx, *url):
		url = ''.join(url)
		if len(url) > 4:
			x = urllib.parse.quote(url)
			await ctx.send("http://metapicz.com/#landing?imgsrc=" + x)
		else:
			for a in ctx.message.attachments:
				x = urllib.parse.quote(a.url)
				await ctx.send("http://metapicz.com/#landing?imgsrc=" + x)
##########################################################				
	@commands.command()
	@commands.guild_only()
	async def ezstego(self,ctx):
		await ctx.send("https://www.secsy.net/easy_stegoCTF")
##########################################################
	@commands.command()
	@commands.guild_only()
	async def pigpen(self,ctx):
		await ctx.send("https://cdn.discordapp.com/attachments/690040647016906757/690215389137076251/8550539_orig.png")
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
	@commands.command()
	@commands.guild_only()
	async def az26(self, ctx, f, *s):
		s = ' '.join(s)
		if pipe in s:
			pp = ProcessPipe("az26 {} {}".format(f,s))
			output = pp.getString()
		else:
			output = do_az26(f,s)
		await ctx.send(output)
	pass
##########################################################
	@commands.command()
	@commands.guild_only()
	async def atbash(self, ctx, f, *s):
		s = ' '.join(s)
		if pipe in s:
			pp = ProcessPipe("atbash {} {}".format(f,s))
			output = pp.getString()
		else:
			output = do_atbash(f,s)
		await ctx.send(output)
	pass
	@commands.command()
	@commands.guild_only()
	async def trans(self, ctx, f, *s):
		s = ' '.join(s)
		if pipe in s:
			pp = ProcessPipe("trans {} {}".format(f,s))
			output = pp.getString()
		else:
			output = do_trans(f,s)
		await ctx.send(output)
	pass
	@commands.command()
	@commands.guild_only()
	async def rails(self, ctx, f, c, *s):
		s = ' '.join(s)
		print(f,c,s)
		output = do_rails(f,c,s)
		await ctx.send(output)
	pass
##########################################################
def setup(bot):
	bot.add_cog(CTFUtility(bot))


