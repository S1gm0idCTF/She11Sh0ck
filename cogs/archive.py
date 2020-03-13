import discord
from discord.ext import commands
from datetime import datetime
class betterEmbeds():
    def __init__(self, category):
        self.embed = discord.Embed(title="# {}".format(str(category)),description="### Created: {}".format(str(datetime.now())),color=0xFF0000)
        self.destination = ''
        self.length = 0 
        self.objectCount = 0 

    def test_embed(self, bodyLength):
        print(1)
        discordConstraints = {"maxCharCount" : 6000, "maxFieldCount": 10}
        if (self.length + bodyLength <= discordConstraints["maxCharCount"]) and (self.objectCount + 1 <= discordConstraints['maxFieldCount']): 
            return True
        else:
            return False

    def reInitialize(self,textChannelName):
        self.embed = discord.Embed(title="# {}".format(str(textChannelName)),description="### Created: {}".format(str(datetime.now())),color=0xFF0000)
        self.length = 0
        self.objectCount = 0

    async def add_field(self, textChannelName, body):
        if not self.test_embed(len(body)):
            print("FAILED")
            #Failed Constraint Check
            if self.destination == '':
                print("I don't know where to send this :/")
            else:
                self.send_message()
                self.reInitialize(str(textChannelName))
        self.length = self.length + len(body)
        self.objectCount = self.objectCount + 1 
        self.embed.add_field(name=str("### " + textChannelName),value=body + "\n", inline=False)

    def add_destination(self,destination):
        print("Destination SET: " + str(destination))
        self.destination = destination

    async def send_message(self):
        self.destination.send(embed=self.embed)
        


class archiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def archive(self, ctx, category):
	# merging doesn't delete the originals in case of an accidental merge
        print("merging category: " + category)
        categoryObject = discord.utils.get(ctx.guild.channels, name=str(category))
        
        embed = betterEmbeds(str(category))

        exportWriteup = ""
        #if discord.utils.get(ctx.guild.channels, name=category + "-archive") is None:
        #await ctx.guild.create_text_channel(category + "-archive",category=discord.utils.get(ctx.guild.categories, name="ARCHIVE"))
        archive_channel =  self.bot.get_channel(discord.utils.get(ctx.guild.channels, name=category + "-archive").id)
        print(str(archive_channel)+ "!")
        embed.add_destination(archive_channel)
        embed.add_field("catchat", "test")
        await embed.send_message()
        i = 0
        for textChannel in categoryObject.channels:
            if i > 5:
                embed.send_message()
                i = 0
            if str(textChannel.type) == "text":
                print(str(textChannel.name))
                channelWriteup = ""
                messages = await textChannel.history().flatten() #fetch all messages in channel.
                m = [x.content for x in messages][::-1]  # reverse messages

                for body in m:
                    channelWriteup = channelWriteup + " - " + body + "\n"
                embed.add_field(textChannel.name, channelWriteup)
            i = i + 1
        if i != 1:
            embed.send_message()
        #else:
        await ctx.send(
            "This CTF has already been merged or something has gone very, very wrong :("
        )
        exportWriteup = ""
        pass

def setup(bot):
    bot.add_cog(archiveCog(bot))