import json
from errors import sendErrorMessage
import discord
from discord.ext import commands
from etc.betterEmbeds import sendEmbed
import sql
from dbhandler import database

class CTFSetup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	@commands.guild_only()
	async def integrityCheck(self, ctx):
		#Checks if Guild exists in DB
		guilds = await sql.db.getGuildByID(ctx.guild.id)
		
		if guilds == None:
			await sql.db.addGuild(ctx.guild.id, ctx.guild.name)
			print("GUILD ERROR: " + str(ctx.guild.id))
		elif len(guilds) > 1:
			print("ERROR TOO MANY GUILDS" + str(ctx.guild.id)) 
			#$THIS WILL NEVER HAPPEN, IF DB SET TO UNIQUE.$#
		
	pass
	@commands.command()
	@commands.guild_only()
	async def currentctf(self, ctx):
		ctf = (await sql.db.getCurrentCTFName(await sql.db.getCurrentCTFID(ctx.message.author.id, ctx.guild.id))) #GETS CURRENT CTF NAME
		await sendEmbed(ctx, "Selected CTF", "{} is the current CTF.".format(ctf))
	pass
	
	@commands.command()
	@commands.guild_only()
	async def setctf(self, ctx, *ctf):
		
		if len(await sql.db.getMember(ctx.message.author.id, ctx.guild.id)) < 1:
			await sql.db.addMember(ctx.message.author.id,ctx.guild.id)

		ctfs = await sql.db.getValidCTFIDs(ctx.message.author.id,ctx.guild.id)		
		if len(ctfs) > 0:
			for dbctf in ctfs:
				ctfid, ctfname = dbctf[0],dbctf[1]
				if ctfname == "_".join(ctf).lower():
					await sql.db.updateCTF(ctx.message.author.id, ctx.guild.id, ctfid)
					await sendEmbed(ctx, "UPDATE", "You are now participating in {}".format(ctfname.upper()))
					return
		await sendEmbed(ctx, "ERROR", "The CTF `{}` wasn't found.".format("_".join(ctf).upper()))

	@commands.command()
	@commands.guild_only()
	async def createctf(self, ctx, *ctfname):
		ctf = '_'.join(ctfname).lower()
		ctf = await ctx.guild.create_category(ctf)
		await sql.db.createCTF(ctf.name, ctx.guild.id)

	@commands.command()
	@commands.guild_only()
	async def addQ(self, ctx, *questionTitle):
		questionTitle = "_".join(questionTitle)
		authorid = ctx.message.author.id
		guildid = ctx.guild.id
		ctf = await sql.db.getCurrentCTFName(await sql.db.getCurrentCTFID(authorid, guildid))
		category = discord.utils.get(ctx.guild.categories, name=ctf)
		channel = await ctx.guild.create_text_channel(questionTitle, category=category)
		await sql.db.addQuestion(str(channel.name), await sql.db.getCurrentCTFID(authorid, guildid))

	pass

	@commands.command()
	@commands.guild_only()
	async def markSolved(self, ctx, Q):
		
		await sql.db.setSolved(str(Q), await sql.db.getCurrentCTFID(ctx.message.author.id, ctx.guild.id))

	@commands.command()
	@commands.guild_only()
	async def markUnsolved(self, ctx, Q):
		
		await sql.db.setUnsolved(str(Q), await sql.db.getCurrentCTFID(ctx.message.author.id, ctx.guild.id))

	@commands.command()
	@commands.guild_only()
	async def ctfQs(self, ctx):
		i = 0
		send = ""
		questionList = await sql.db.getCTFQuestions(await sql.db.getCurrentCTFID(ctx.message.author.id, ctx.message.guild.id))
		for question in questionList:
			if question[1] > 0:
				send += "[{}] ".format(i) + "~~**"  + question[0] + "**~~\n"
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
		ctf = await sql.db.getCurrentCTFName(await sql.db.getCurrentCTFID(authorid, guildid))
		category = await discord.utils.get(ctx.guild.categories, name=ctf)
		channel = await discord.utils.get(name=Q, category=category)
		await channel.delete()
		await sql.db.deleteQ(str(channel.name), await sql.db.getCurrentCTFID(authorid, guildid))
	
	@commands.command(hidden=True)
	@commands.guild_only()
	@commands.is_owner()
	async def deletectf(self, ctx, *name):
		categoryName = "_".join(name).lower()
		channel = discord.utils.get(ctx.guild.categories, name=categoryName)
		if channel != None:
			for channels in channel.channels:
				await channels.delete()
			await channel.delete()
		await sql.db.deleteCTF(categoryName, ctx.guild.id)

def setup(bot):
	bot.add_cog(CTFSetup(bot))