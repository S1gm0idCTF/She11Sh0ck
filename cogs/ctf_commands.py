import base64

import discord
from discord.ext import commands


class ctfUtility(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	async def b64Decode(self, ctx, string):
		await ctx.send(base64.b64decode(string).decode("utf-8"))

	@commands.command()
	@commands.guild_only()
	async def b64Encode(self, ctx, string):
		await ctx.send(base64.b64encode(string.encode()).decode("utf-8"))

	@commands.command()
	@commands.guild_only()
	async def binaryDecode(self, ctx, binary_string):
		binary_string = binary_string.replace(" ", "")
		print(binary_string)
		string = "".join(
			chr(int(binary_string[i * 8 : i * 8 + 8], 2))
			for i in range(len(binary_string) // 8)
		)
		await ctx.send(string)


def setup(bot):
	bot.add_cog(ctfUtility(bot))
