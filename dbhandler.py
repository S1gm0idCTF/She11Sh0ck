import asyncio
import aiomysql
from creds import getdb

# Connect to server
class database:
	def __init__(self):
		print("Starting...")

	async def createPool(self, loop):
		dbcreds = getdb()
		self.pool = await aiomysql.create_pool(
			host=dbcreds["host"],
			port=dbcreds["port"],
			user=dbcreds["user"],
			password=dbcreds["password"],
			db=dbcreds["db"],
			loop=loop,
		)

	async def getUserCTFID(self, discordID, guildID):
		sql = "SELECT activectf FROM members where `uuid` = %d and `guildid` = %d" % (
			int(discordID),
			int(guildID),
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				(r) = await cur.fetchone()
				return r[0]
		# self.pool.close()
		# await self.pool.wait_closed()
	async def getCTFID(self, name, guildID):
		sql = "SELECT ctfid FROM ctfs where `name` = '{}' and `guildid` = '{}'".format(
			str(name),
			int(guildID),
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				(r) = await cur.fetchone()
				return r[0]

	async def getCTFName(self, CTFID):
		sql = "SELECT name FROM ctfs where `ctfid` = %d" % (int(CTFID))
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				(r) = await cur.fetchone()
				return r[0]
		# self.pool.close()
		# wait self.pool.wait_closed()

	async def getCTFQuestions(self, CTFID):
		sql = "SELECT name,Solved FROM ctfQuestions where `ctfid` = %d" % (int(CTFID))
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				(r) = await cur.fetchall()
				return r
		# self.pool.close()
		# await self.pool.wait_closed()

	async def getValidCTFIDs(self, DiscordID, GuildID):
		sql = "SELECT ctfs.ctfid,ctfs.name FROM members INNER JOIN ctfs ON ctfs.guildid=members.guildid WHERE ctfs.guildid = members.guildid and members.uuid = {} and members.guildid = {}".format(
			int(DiscordID), int(GuildID)
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				(r) = await cur.fetchall()
				return r
		# self.pool.close()
		# await self.pool.wait_closed()

	async def updateCTF(self, DiscordID, GuildID, CTFID):
		sql = "UPDATE `members` SET `activectf`={} WHERE uuid={} and guildid={}".format(
			int(CTFID), int(DiscordID), int(GuildID)
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				await conn.commit()
		# self.pool.close()
		# await self.pool.wait_closed()

	async def createCTF(self, ctfName, guildID):
		print(ctfName)
		sql = "INSERT INTO ctfs (name, guildid) VALUES ('{}','{}')".format(
			str(ctfName), int(guildID)
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				await conn.commit()

	async def deleteCTF(self, ctfName, guildID):
		print("Goodbye {}".format(ctfName))
		sql = "DELETE FROM `ctfs` WHERE name = '{}' and guildid = '{}'".format(
			str(ctfName), int(guildID)
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				await conn.commit()
			# self.pool.close()
			# await self.pool.wait_closed()

	async def getGuildByID(self, guildid):
		sql = "SELECT guildid, guildname from guilds where guildid={}".format(
			int(guildid)
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				return await cur.fetchone()

		# self.pool.close()
		# await self.pool.wait_closed()

	async def getMember(self, uuid, guildid):
		sql = "SELECT id from members where uuid = {} and guildid={}".format(
			int(uuid), int(guildid)
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				return await cur.fetchone()

		# self.pool.close()
		# await self.pool.wait_closed()

	async def addMember(self, uuid, guildid):
		sql = "INSERT INTO members (uuid,guildid, activectf) VALUES ('{}','{}','{}')".format(
			int(uuid), int(guildid), 0
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				await conn.commit()

		# self.pool.close()
		# await self.pool.wait_closed()

	async def addGuild(self, guildid, guildname):
		sql = "INSERT INTO guilds (guildid, guildname) VALUES ('{}','{}')".format(
			int(guildid), str(guildname)
		)
		print(sql)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				await conn.commit()

		# self.pool.close()
		# await self.pool.wait_closed()

	async def addQuestion(self, questionName, CTFID):
		sql = "INSERT INTO ctfQuestions (name, ctfid, Solved) VALUES ('{}','{}', '{}')".format(
			str(questionName), int(CTFID), 0
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				await conn.commit()

		# self.pool.close()
		# await self.pool.wait_closed()

	async def updateQuestionState(self, questionName, CTFID, state):
		sql = "UPDATE `ctfQuestions` SET `Solved`='{}' WHERE name='{}' and CTFID='{}'".format(
			int(state), str(questionName), int(CTFID)
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				await conn.commit()

		# self.pool.close()
		# await self.pool.wait_closed()
	async def setSolved(self, questionName, CTFID):
		await self.updateQuestionState(questionName, CTFID, 1)

	async def setUnsolved(self, questionName, CTFID):
		await self.updateQuestionState(questionName, CTFID, 0)

	async def delQuestion(self, questionName, CTFID):
		sql = "DELETE FROM `ctfQuestions` WHERE name='{}' and CTFID='{}' ".format(
			str(questionName), int(CTFID)
		)
		async with self.pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				await conn.commit()

		# self.pool.close()
		# await self.pool.wait_closed()

