import discord
from discord.ext import commands

class errorCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, errormsg):
		await ctx.message.delete()
		"""The event triggered when an error is raised while invoking a command.
			ctx   : Context
			error : Exception"""
		error = sendErrorMessage(ctx)
		await error.sendError(errormsg)

def setup(bot):
	bot.add_cog(errorCog(bot))
