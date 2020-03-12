import discord
from discord.ext import commands
from datetime import datetime

class archiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def archive(self, ctx, category):
	# merging doesn't delete the originals in case of an accidental merge
        print("merging category: " + category)
        categoryObject = discord.utils.get(ctx.guild.channels, name=category)
        embed = discord.Embed(
            title="# {}".format(str(category)),
            description="### Created: {}".format(str(datetime.now())),
            color=0xFF0000,
        )
        exportWriteup = ""
        if discord.utils.get(ctx.guild.channels, name=category + "-archive") is None:
            await ctx.guild.create_text_channel(
                category + "-archive",
                category=discord.utils.get(ctx.guild.categories, name="ARCHIVE"),
            )
            archive_channel = self.bot.get_channel(
                discord.utils.get(ctx.guild.channels, name=category + "-archive").id
            )
            i = 0
            for textChannel in categoryObject.channels:
                if i > 5:
                    await archive_channel.send(embed=embed)
                    embed = discord.Embed(
                        title="# {}".format(str(category)),
                        description="## Created: {}".format(str(datetime.now())),
                        color=0xFF0000,
                    )
                    i = 0
                if str(textChannel.type) == "text":
                    print(str(textChannel.name))
                    channelWriteup = ""
                    messages = await textChannel.history().flatten()
                    m = [x.content for x in messages][::-1]  # reverse messages

                    for body in m:
                        channelWriteup = channelWriteup + " - " + body + "\n"
                    embed.add_field(
                        name=str("### " + textChannel.name),
                        value=channelWriteup + "\n",
                        inline=False,
                    )
                i = i + 1
            if i != 1:
                await archive_channel.send(embed=embed)
        else:
            await ctx.send(
                "This CTF has already been merged or something has gone very, very wrong :("
            )
        exportWriteup = ""
        pass

def setup(bot):
    bot.add_cog(archiveCog(bot))