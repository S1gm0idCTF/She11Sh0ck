import discord
from discord.ext import commands

from errors import sendErrorMessage
from etc.betterEmbeds import sendEmbed

class MiscCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def bugReport(self, ctx):
		embed = discord.Embed(
					title="BUG REPORT FORM", color=0xA292C1
				)
		embed.add_field(name="How to Report", value="Thank you so much for wanting to report a bug! In order to contact the developers, please find us @BlackCoffee#2718 or @a.lil.sus#7939 or you can email us at S1gm0idCTF@gmail.com")
		embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2016/03/31/21/59/bug-1296767_960_720.png")
		await ctx.send(embed=embed)
		
	@commands.command()
	async def suggest(self, ctx):
		embed = discord.Embed(
					title="SUGGESTION FORM", color=0xA292C1
				)
		embed.add_field(name="How to Suggest", value="Thank you so much for wanting to provide a suggestion! In order to contact the developers, please find us @BlackCoffee#2718 or @a.lil.sus#7939 or you can email us at S1gm0idCTF@gmail.com")
		# embed.set_thumbnail(url="#")
		await ctx.send(embed=embed)

def setup(bot):

	bot.add_cog(MiscCommands(bot))
