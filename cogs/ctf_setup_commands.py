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
			ctf = await sql.db.getCTFName(
				await sql.db.getUserCTFID(ctx.message.author.id, ctx.guild.id)
			)  # GETS CURRENT CTF NAME
			if ctf is not None:
				await sendEmbed(ctx, "Selected CTF", "You are now playing: {}.".format(ctf))
			else:
				error = sendErrorMessage(ctx)
				await error.sendError("E_CTF_NOT_SET")
		except:
			error = sendErrorMessage(ctx)
			await error.sendError("E_CTF_NOT_IN_DB")

	@commands.command()
	@commands.guild_only()
	async def setctf(self, ctx, *ctf):

		if await sql.db.getMember(ctx.message.author.id, ctx.guild.id) is None:
			await sql.db.addMember(ctx.message.author.id, ctx.guild.id)

		ctf = "_".join(ctf).lower().strip()
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
		ctf = "_".join(ctfname).lower().strip()
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
		questionTitle = "_".join(questionTitle).lower().strip()
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		try:
			for Q in await sql.db.getCTFQuestions(
				await sql.db.getUserCTFID(authorid, guildid)
			):
				if questionTitle.lower() == Q[0]:
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
	async def markSolved(self, ctx, Q):
		questionTitle = Q.replace(" ", "_").lower().strip()
		authorid = ctx.message.author.id
		guildid = ctx.guild.id

		for Q in await sql.db.getCTFQuestions(
			await sql.db.getUserCTFID(authorid, guildid)
		):
			if questionTitle == Q[0]:
				await sql.db.setSolved(
					Q[0], await sql.db.getUserCTFID(ctx.message.author.id, ctx.guild.id)
				)
				embed = discord.Embed(
					title=ctx.author.name + " marked " + Q[0] + " as solved!",
					color=0x9400D3,
				)
				embed.set_thumbnail(
					url="https://res-4.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1397182843/e121315c5563525c7197fadf36fcbb9a.png"
				)

				await ctx.send("@here")
				await ctx.send(embed=embed)
				return
		error = sendErrorMessage(ctx)
		await error.sendError("E_Q_NOT_FOUND")

	@commands.command()
	@commands.guild_only()
	async def markUnsolved(self, ctx, Q):
		questionTitle = Q.replace(" ", "_").lower().strip()
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		for Q in await sql.db.getCTFQuestions(
			await sql.db.getUserCTFID(authorid, guildid)
		):
			if questionTitle == Q[0]:
				await sql.db.setUnsolved(
					str(Q[0]),
					await sql.db.getUserCTFID(ctx.message.author.id, ctx.guild.id),
				)
				return
		error = sendErrorMessage(ctx)
		await error.sendError("E_Q_NOT_FOUND")

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
		questionTitle = Q.replace(" ", "_").lower().strip()
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		try:
			for Q in await sql.db.getCTFQuestions(
				await sql.db.getUserCTFID(authorid, guildid)
			):
				print(questionTitle)
				print(Q[0])
				if questionTitle == Q[0]:
					ctf = await sql.db.getCTFName(
						await sql.db.getUserCTFID(authorid, guildid)
					)
					category = discord.utils.get(ctx.guild.categories, name=ctf)
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
		categoryName = "_".join(name).lower().strip()
		print(categoryName)
		category = discord.utils.get(ctx.guild.categories, name=categoryName)
		if category != None:
			for channel in category.channels:
				await channel.delete()
			await category.delete()
		await sql.db.deleteCTF(categoryName, ctx.guild.id)


def setup(bot):
	bot.add_cog(CTFSetup(bot))

