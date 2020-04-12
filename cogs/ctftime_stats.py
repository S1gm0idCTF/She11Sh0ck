import json
import time

import discord
import requests
import urllib3
from discord.ext import commands

import sql
from errors import sendErrorMessage
from etc.betterEmbeds import sendEmbed


class CTFSetup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	async def teamstats(self, ctx):
		if (await sql.db.getGuildTeamID(ctx.guild.id))[0] == 0:
			error = sendErrorMessage(ctx)
			await error.sendError("E_TEAM_ID_NOT_SET")
		else:
			try:
				teamid = str((await sql.db.getGuildTeamID(ctx.guild.id))[0])
				url = "https://ctftime.org/api/v1/teams/" + teamid + "/"
				headers = {
					"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
				}

				data = requests.get(url, headers=headers)
				data = data.json()

				global_rating_place = data["rating"][0]["2020"]["rating_place"]
				global_rating_points = round(
					data["rating"][0]["2020"]["rating_points"], 3
				)
				team_name = data["name"]
				embed = discord.Embed(
					title="Information about " + team_name, color=0xA292C1
				)
				embed.add_field(name="__Global Ranking__", value=global_rating_place)
				embed.add_field(name="__Points__", value=global_rating_points)
				embed.set_thumbnail(url="https://ctftime.org/static/img/s/16x16.png")

				await ctx.send(embed=embed)
			except:
				error = sendErrorMessage(ctx)
				await error.sendError("E_TEAM_ID_WRONG")

				

	@commands.command()
	@commands.guild_only()
	async def setid(self, ctx, teamid):
		await sql.db.setGuildTeamID(teamid, ctx.guild.id)


def setup(bot):
	bot.add_cog(CTFSetup(bot))
