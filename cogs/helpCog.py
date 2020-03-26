import discord
from discord.ext import commands

from errors import sendErrorMessage
from etc.betterEmbeds import sendEmbed


class helpCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	async def help(self, ctx, *p):

		if p != ():
			if p[0].lower() == "admin" or p[0].lower() == "0":
				await sendEmbed(
					ctx,
					"Help!",
					"**Admin**\n"
					+ "\n ⯍Creates a new category with the name given, which is dynamically addressed as a new 'CTF'⯍\n"
					+ "`!ctf createctf [ctfname]`\n"
					+ "\n ⯍Deletes the CTF server from your Discord server, and the bots backend.⯍\n"
					+ "`!ctf deletectf [ctfname]`\n"
					+ "\n ⯍Archives the CTF by collapsing every text channel into a single channel in the category #ARCHIVE⯍\n"
					+ "`!ctf archive [ctfname]`\n",
				)

			elif p[0].lower() == "player" or p[0].lower() == "1":
				await sendEmbed(
					ctx,
					"Help!",
					"**Player**\n"
					+ "\n⯍Adds a Question to the active CTF server⯍\n"
					+ "`!ctf addQ [Question Name] `\n"
					+ "\n⯍Deletes a Question from the active CTF server⯍\n"
					+ "`!ctf deleteQ [Question Name]`\n"
					+ "\n⯍Returns a list of questions that are in the selected CTF server⯍\n"
					+ "`!ctf ctfQs`\n"
					+ "\n⯍Sets your CTF to the selected CTF⯍\n"
					+ "`!ctf setctf [ctfname]`\n"
					+ "\n⯍Checks what CTF you are currently playing⯍\n"
					+ "`!ctf myctf`\n"
					+ "\n⯍Marks the Question as solved, in the selected CTF server⯍\n"
					+ "`!ctf markSolved [Question Name]`\n"
					+ "\n⯍Marks the Question as unsolved, in the selected CTF server⯍\n"
					+ "`!ctf markUnsolved [Question Name]`\n",
				)

			elif (
				p[0].lower() == "cryptography"
				or p[0].lower() == "crypto"
				or p[0].lower() == "2"
			):
				await sendEmbed(
					ctx,
					"Help!",
					"**Cryptography**\n"
					+ "⯍The following Cryptographic functions permit for piping from one-to-another, i.e. \n`!ctf b64 -e **input** | hex -e | trans -join | trans -s4`\n"
					+ "\n⯍Atbash Encoder⯍\n"
					+ "`!ctf atbash (-e or -d) **input**`\n"
					+ "\n⯍AZ26 Encoder⯍\n"
					+ "`!ctf az26 (-e or -d) **input**`\n"
					+ "\n⯍Base16 Encoder⯍\n"
					+ "`!ctf b16 (-e or -d) **input**`\n"
					+ "\n⯍Base32 Encoder⯍\n"
					+ "`!ctf b32 (-e or -d) **input**`\n"
					+ "\n⯍Base64 Encoder⯍\n"
					+ "`!ctf b64 (-e or -d) **input**`\n"
					+ "\n⯍Binary Encoder⯍\n"
					+ "`!ctf binary (-e or -d) **input**`\n"
					+ "\n⯍Hex Encoder⯍	  \n"
					+ "`!ctf hex (-e or -d) **input**`\n"
					+ "\n⯍Transforms Text valid parameters are:⯍\n*-upper, -lower, -t, -rev(erse), -join, -s[int]*\n"
					+ "`!ctf trans (parameter) **input**`\n",
				)
			elif p[0].lower() == "other" or p[0].lower() == "3":
				await sendEmbed(
					ctx,
					"Help!",
					"**Other**\n"
					+ "\n⯍Rail Cipher (Zigzag Cipher)⯍\n"
					+ "`!ctf rails (-e or -d) [int] **input**`\n"
					+ "\n⯍Counts the characters in a message⯍\n"
					+ "`!ctf count **input** `\n"
					+ "\n⯍Exiftool⯍\nRunning this command, and uploading an image, or using the optional URL parameter, will encode the link and pass it to a third-party exiftool website."
					+ "\n`!ctf exiftool ([URL] or [attach file])`\n"
					+ "\n⯍Online Binwalk⯍\n"
					+ "`!ctf ezstego`\n"
					+ "\n⯍PigPen Cipher⯍\n"
					+ "`!ctf pigpen`\n",
				)

		else:
			await sendEmbed(
				ctx,
				"Help!",
				"*!ctf help [Category]*\n ```fix\n ⮞ Admin```\n ```fix\n ⮞ Player```\n ```fix\n ⮞ Cryptography```\n ```fix\n ⮞ Other```\n https://s1gm0idctf.github.io/bot ",
			)

	pass


def setup(bot):

	bot.add_cog(helpCog(bot))
