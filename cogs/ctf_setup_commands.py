import json

import discord
from discord.ext import commands

import sql
from errors import sendErrorMessage
from etc.betterEmbeds import sendEmbed


class CTFSetup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	async def currentctf(self, ctx):
		ctf = await sql.db.getCTFName(
			await sql.db.getUserCTFID(ctx.message.author.id, ctx.guild.id)
		)  # GETS CURRENT CTF NAME
		if ctf is not None:
			await sendEmbed(ctx, "Selected CTF", "You are now playing: {}.".format(ctf))
		else:
			error = sendErrorMessage(ctx)
			await error.sendError("E_NOT_SET")

	@commands.command()
	@commands.guild_only()
	async def setctf(self, ctx, *ctf):

		if await sql.db.getMember(ctx.message.author.id, ctx.guild.id) is None:
			await sql.db.addMember(ctx.message.author.id, ctx.guild.id)

		ctf = "_".join(ctf).lower()
		try:
			new_ctf_id = await sql.db.getCTFID(ctf, ctx.guild.id)
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_NOT_FOUND")
			return

		await sql.db.updateCTF(ctx.message.author.id, ctx.guild.id, new_ctf_id)
		await sendEmbed(
			ctx, "UPDATE", "You are now participating in: {}".format(ctf.upper()),
		)
		return

	@commands.command()
	@commands.guild_only()
	async def createctf(self, ctx, *ctfname):
		ctf = "_".join(ctfname).lower()
		ctf = await ctx.guild.create_category(ctf)
		await sql.db.createCTF(ctf.name, ctx.guild.id)
		await self.setctf(ctx, ctf.name)

	@commands.command()
	@commands.guild_only()
	async def addQ(self, ctx, *questionTitle):
		questionTitle = "_".join(questionTitle)
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		ctf = await sql.db.getCTFName(await sql.db.getUserCTFID(authorid, guildid))
		category = discord.utils.get(ctx.guild.categories, name=ctf)
		channel = await ctx.guild.create_text_channel(questionTitle, category=category)
		await sql.db.addQuestion(
			str(channel.name), await sql.db.getUserCTFID(authorid, guildid)
		)

	pass

	@commands.command()
	@commands.guild_only()
	async def markSolved(self, ctx, Q):

		await sql.db.setSolved(
			str(Q), await sql.db.getUserCTFID(ctx.message.author.id, ctx.guild.id)
		)

	@commands.command()
	@commands.guild_only()
	async def markUnsolved(self, ctx, Q):

		await sql.db.setUnsolved(
			str(Q), await sql.db.getUserCTFID(ctx.message.author.id, ctx.guild.id)
		)

	@commands.command()
	@commands.guild_only()
	async def ctfQs(self, ctx):
		i = 0
		send = ""
		questionList = await sql.db.getCTFQuestions(
			await sql.db.getUserCTFID(ctx.message.author.id, ctx.message.guild.id)
		)
		for question in questionList:
			if question[1] > 0:
				send += "[{}] ".format(i) + "~~**" + question[0] + "**~~\n"
			else:
				send += "[{}] ".format(i) + question[0] + "\n"
			i = i + 1

		await sendEmbed(ctx, "Current Questions:", send)
		pass

	@commands.command()
	@commands.guild_only()
	async def deleteQ(self, ctx, Q):
		Q = "_".join(Q)
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		ctf = await sql.db.getCTFName(await sql.db.getUserCTFID(authorid, guildid))

		category = discord.utils.get(ctx.guild.categories, name=ctf)
		channel = discord.utils.get(ctx.guild.text_channels, category=category, name=Q)
		await channel.delete()
		await sql.db.delQuestion(
			str(channel.name), await sql.db.getUserCTFID(authorid, guildid)
		)

	@commands.command(hidden=True)
	@commands.guild_only()
	@commands.is_owner()
	async def deletectf(self, ctx, *name):
		categoryName = "_".join(name).lower()
		category = discord.utils.get(ctx.guild.categories, name=categoryName)
		if category != None:
			for channel in category.channels:
				await channel.delete()
			await category.delete()
			await sql.db.delQuestion(
				str(channel.name), await sql.db.getCTFID(categoryName, ctx.guild.id)
			)
		await sql.db.deleteCTF(categoryName, ctx.guild.id)


def setup(bot):
	bot.add_cog(CTFSetup(bot))
