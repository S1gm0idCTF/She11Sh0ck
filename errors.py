import asyncio

import discord
from discord.ext import commands

timeout = 5


class sendErrorMessage:
	def __init__(self, channel):
		self.embed = discord.Embed(
			title="# {}".format(str(channel)),
			description="!Something Went Wrong",
			color=0x9400D3,
		)
		self.channel = channel

	async def sendError(self, errorcode):
		if errorcode == "" or str(errorcode).startswith("E_"):
			errorcode = self.get_error(errorcode)
		self.embed.add_field(name="Error:", value=errorcode)
		self.embed.set_thumbnail(
			url="https://cdn.pixabay.com/photo/2017/02/12/21/29/false-2061131_960_720.png"
		)
		message = await self.channel.send(embed=self.embed)
		await asyncio.sleep(timeout)
		await message.delete()
	def get_error(self, errorcode):
		errors = {
			"E_INVALID_COMMAND": "I've never heard of that command before, have you even read my README.md :(",
			"E_INVALID_PARAMS": "Unfortunately more parameters were expected for that command. If you're still unsure, consider `!ctf help`.",
			"E_CHANNEL_NOT_FOUND": "That channel doesn't seem to exist. I'll look again, but I might just be blind. ",
			"E_CHANNEL_NOT_SET": "I really can't help you send messages to a channel that isn't defined. If you don't know what I should do, then how should I?",
			"E_CTF_NOT_SET": "To my knowledge there is no ongoing CTF, perhaps you should consider setting one using `!ctf create [ctfname]` or `!ctf setCTF [ctfname]`.",
			"E_CTF_NOT_FOUND": "That CTF doesn't exist, maybe you mispelled it.",
			"E_CTF_NOT_IN_DB": "It looks like the CTF you are in is not in our database, perhaps it was deleted or you didn't create it yet.",
			"E_CTF_ALREADY_EXISTS": "That CTF already exists, maybe you should `!ctf setCTF [ctfname]`",
			"E_CTF_ALREADY_MERGED": "This CTF has already been merged or something has gone very, very wrong",
			"E_Q_NOT_FOUND": "That Q doesn't exist, maybe you mispelled it.",
			"E_Q_ALREADY_EXISTS": "A Q with that name already exists.",
			"E_TEAM_ID_NOT_SET": "You haven't set your team ID. Please set it with !ctf setid [id]",
			"E_TEAM_ID_WRONG" : "CTFTime doesn't have a team with this ID. Try re-entering your team ID with !ctf setid [id]. You can find your id in the URL of your team's CTFTime page.",
			"E_GENERIC": "An unknown error occured. The developers have been notified.",
			"": "E_[...] Expectant an Error, no errorcode defined.",
		}
		return errors[errorcode]

