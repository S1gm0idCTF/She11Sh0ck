import json
import time

import discord
import requests
import urllib3
from discord.ext import commands

from errors import sendErrorMessage


class CTFSetup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	async def teamstats(self, ctx):
		with open("server_config.json", "r") as f:
			config = json.load(f)
		if "teamID" not in config[str(ctx.guild.id)]["info"].keys():
			error = sendErrorMessage(ctx)
			await error.sendError("E_TEAM_ID_NOT_SET")
		else:
			url = (
				"https://ctftime.org/api/v1/teams/"
				+ config[str(ctx.guild.id)]["info"]["teamID"]
				+ "/"
			)
			headers = {
				"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
			}

			data = requests.get(url, headers=headers)
			data = data.json()

			global_rating_place = data["rating"][0]["2020"]["rating_place"]
			global_rating_points = round(data["rating"][0]["2020"]["rating_points"], 3)
			team_name = data["name"]

			embed = discord.Embed(
				title="Information about " + team_name, color=0x9400D3
			)
			embed.add_field(name="__Global Ranking__", value=global_rating_place)
			embed.add_field(name="__Points__", value=global_rating_points)
			embed.set_thumbnail(url="https://ctftime.org/static/img/s/16x16.png")

			await ctx.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	async def setID(self, ctx, teamID):
		with open("server_config.json", "r") as f:
			config = json.load(f)

		config[str(ctx.guild.id)]["info"]["teamID"] = str(teamID.strip())

		with open("server_config.json", "w") as f:
			json.dump(config, f, indent=4)


def setup(bot):
	bot.add_cog(CTFSetup(bot))
