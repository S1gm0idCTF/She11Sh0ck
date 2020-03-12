import discord
from discord.ext import commands


class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True)
	@commands.is_owner()
	async def load(self, ctx, *, cog: str):
		"""Command which Loads a Module.
		Remember to use dot path. e.g: cogs.owner"""

		try:
			self.bot.load_extension(cog)
		except Exception as e:
			await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
		else:
			await ctx.send("**`SUCCESS`**")

	@commands.command(hidden=True)
	@commands.is_owner()
	async def unload(self, ctx, *, cog: str):
		"""Command which Unloads a Module.
		Remember to use dot path. e.g: cogs.owner"""

		try:
			self.bot.unload_extension(cog)
		except Exception as e:
			await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
		else:
			await ctx.send("**`SUCCESS`**")

	@commands.command(hidden=True)
	@commands.is_owner()
	async def reload(self, ctx, *, cog: str):
		"""Command which Reloads a Module.
		Remember to use dot path. e.g: cogs.owner"""

		try:
			self.bot.reload_extension(cog)
		except Exception as e:
			await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
		else:
			await ctx.send("**`SUCCESS`**")


def setup(bot):
	bot.add_cog(AdminCog(bot))
