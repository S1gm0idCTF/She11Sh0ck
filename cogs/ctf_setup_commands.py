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
	async def myctf(self, ctx):
		try:
			if await sql.db.getUserCTFID(ctx.message.author.id, ctx.guild.id) == 0:
				error = sendErrorMessage(ctx)
				await error.sendError("E_CTF_NOT_SET")
			else:
				ctf = await sql.db.getCTFName(
					await sql.db.getUserCTFID(ctx.message.author.id, ctx.guild.id)
				)  # GETS CURRENT CTF NAME
				if ctf is not None:
					await sendEmbed(
						ctx, "Selected CTF", "You are now playing: {}.".format(ctf)
					)
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_NOT_IN_DB")

	@commands.command()
	@commands.guild_only()
	async def setctf(self, ctx, *ctf):

		if await sql.db.getMember(ctx.message.author.id, ctx.guild.id) is None:
			await sql.db.addMember(ctx.message.author.id, ctx.guild.id)

		ctf = "-".join(ctf).lower().strip()
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
	async def setdefaultctf(self, ctx, *ctf):

		if await sql.db.getMember(ctx.message.author.id, ctx.guild.id) is None:
			await sql.db.addMember(ctx.message.author.id, ctx.guild.id)

		ctf = "-".join(ctf).lower().strip()
		try:
			new_ctf_id = await sql.db.getCTFID(ctf, ctx.guild.id)
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_NOT_FOUND")
			return
		
		for ele in await sql.db.getAllMembers(ctx.guild.id):
			await sql.db.updateCTF(ele[1], ctx.guild.id, new_ctf_id)

		await ctx.send("@everyone")
		await sendEmbed(
			ctx, "UPDATE", "The default CTF is now: {}".format(ctf),
		)
		return

	@commands.command()
	@commands.guild_only()
	async def createctf(self, ctx, *ctfname):
		ctf = "-".join(ctfname).lower().strip()
		# returns all CTF names and IDs in a server
		# (id, 'name')
		ctf_list = await sql.db.getValidCTFIDs(ctx.message.author.id, ctx.guild.id)
		for db_ctf in ctf_list:
			if ctf == db_ctf[1]:
				error = sendErrorMessage(ctx)
				await error.sendError("E_CTF_ALREADY_EXISTS")
				return

		ctf = await ctx.guild.create_category(ctf)
		await sql.db.createCTF(ctf.name, ctx.guild.id)
		await self.setctf(ctx, ctf.name)

	@commands.command()
	@commands.guild_only()
	async def addQ(self, ctx, *questionTitle):
		questionTitle = "-".join(questionTitle).lower().strip()
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		try:
			print(
				await sql.db.getCTFQuestions(
					await sql.db.getUserCTFID(authorid, guildid)
				)
			)
			if questionTitle in [
				Q[0]
				for Q in await sql.db.getCTFQuestions(
					await sql.db.getUserCTFID(authorid, guildid)
				)
			]:
				error = sendErrorMessage(ctx)
				await error.sendError("E_Q_ALREADY_EXISTS")
				return

			ctf = await sql.db.getCTFName(await sql.db.getUserCTFID(authorid, guildid))
			category = discord.utils.get(ctx.guild.categories, name=ctf)
			channel = await ctx.guild.create_text_channel(
				questionTitle, category=category
			)
			await sql.db.addQuestion(
				str(channel.name), await sql.db.getUserCTFID(authorid, guildid)
			)
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_NOT_IN_DB")

	@commands.command()
	@commands.guild_only()
	async def markSolved(self, ctx, *Q):
		questionTitle = "-".join(Q).lower().strip()
		authorid = ctx.message.author.id
		guildid = ctx.guild.id

		try:
			await sql.db.setSolved(
				questionTitle, await sql.db.getUserCTFID(authorid, guildid)
			)
			embed = discord.Embed(
				title=ctx.author.name + " marked " + questionTitle + " as solved!",
				color=0xA292C1,
			)
			embed.set_thumbnail(
				url="https://res-4.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1397182843/e121315c5563525c7197fadf36fcbb9a.png"
			)

			await ctx.send("@here")
			await ctx.send(embed=embed)
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_Q_NOT_FOUND")

	@commands.command()
	@commands.guild_only()
	async def markUnsolved(self, ctx, *Q):
		questionTitle = "-".join(Q).lower().strip()
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		try:
			await sql.db.setUnsolved(
				questionTitle, await sql.db.getUserCTFID(authorid, guildid)
			)
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_Q_NOT_FOUND")

	@commands.command()
	@commands.guild_only()
	async def setFlagFormat(self, ctx, *flagFormat):
		flagFormat = "-".join(flagFormat).strip()
		guildid = ctx.guild.id
		authorid = ctx.message.author.id
		try:
			await sql.db.updateFlagFormat(
				flagFormat, await sql.db.getUserCTFID(authorid, guildid)
			)
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_NOT_SET")

	@commands.command()
	@commands.guild_only()
	async def ctfQs(self, ctx):
		send = ""
		questionList = await sql.db.getCTFQuestions(
			await sql.db.getUserCTFID(ctx.message.author.id, ctx.message.guild.id)
		)
		for i, question in enumerate(questionList):
			if question[1] > 0: # if question is solved
				send += "[{}] ".format(i) + "~~**" + question[0] + "**~~\n"
			else:
				send += "[{}] ".format(i) + question[0] + "\n"

		await sendEmbed(ctx, "Current Questions:", send)
		pass

	@commands.command()
	@commands.guild_only()
	async def deleteQ(self, ctx, *Q):
		questionTitle = "-".join(Q).lower().strip()
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		try:
			for Q in await sql.db.getCTFQuestions(
				await sql.db.getUserCTFID(authorid, guildid)
			):
				if questionTitle == Q[0]:
					ctf_name = await sql.db.getCTFName(
						await sql.db.getUserCTFID(authorid, guildid)
					)
					category = discord.utils.get(ctx.guild.categories, name=ctf_name)
					channel = discord.utils.get(
						ctx.guild.text_channels, category=category, name=questionTitle
					)
					await channel.delete()
					await sql.db.delQuestion(
						str(channel.name), await sql.db.getUserCTFID(authorid, guildid)
					)
					return
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_Q_NOT_FOUND")

	@commands.command(hidden=True)
	@commands.guild_only()
	@commands.is_owner()
	async def deletectf(self, ctx, *name):
		categoryName = "-".join(name).lower().strip()
		category = discord.utils.get(ctx.guild.categories, name=categoryName)
		if category != None:
			for channel in category.channels:
				await channel.delete()
			await category.delete()
		await sql.db.deleteCTF(categoryName, ctx.guild.id)


def setup(bot):
	bot.add_cog(CTFSetup(bot))

