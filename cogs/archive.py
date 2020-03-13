import discord
from discord.ext import commands
from datetime import datetime

class betterEmbeds():
    def __init__(self, category):
        self.embed = discord.Embed(title="# {}".format(str(category)),description="### Created: {}".format(str(datetime.now())),color=0xFF0000)
        self.destination = ''
        self.length = 0 
        self.objectCount = 0 

    async def test_embed(self, bodyLength):
        
        if (self.length + bodyLength >= 6000) or (self.objectCount + 1 >= 12): 
            return False
        else:
            return True

    async def reInitialize(self,textChannelName):
        self.embed = discord.Embed(title="# {}".format(str(textChannelName)),description="### Created: {}".format(str(datetime.now())),color=0xFF0000)
        self.length = 0
        self.objectCount = 0

    async def add_field(self, textChannelName, body):
        print(self.objectCount)
        if not await self.test_embed(len(body)):
            print("FAILED")
            #Failed Constraint Check
            if self.destination == '':
                print("I don't know where to send this :/")
            else:
                await self.send_message()
                await self.reInitialize(str(textChannelName))
        self.length = self.length + len(body)
        self.objectCount = self.objectCount + 1 
        self.embed.add_field(name=str("### " + textChannelName),value=body + "\n", inline=False)

    async def add_destination(self,destination):
        print("Destination SET: " + str(destination))
        self.destination = destination

    async def send_message(self):
        await self.destination.send(embed=self.embed)

class archiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def archive(self, ctx, category):
	# merging doesn't delete the originals in case of an accidental merge
        print("[JOB START]: MERGE" + category.upper())
        categoryObject = discord.utils.get(ctx.guild.channels, name=str(category))
        
        embed = betterEmbeds(str(category))

        exportWriteup = ""
        if discord.utils.get(ctx.guild.channels, name=category + "-archive") is None:
            await ctx.guild.create_text_channel(category + "-archive",category=discord.utils.get(ctx.guild.categories, name="ARCHIVE"))
        archive_channel =  self.bot.get_channel(discord.utils.get(ctx.guild.channels, name=category + "-archive").id)    
        await embed.add_destination(archive_channel)
            
            
        i = 0
        for textChannel in categoryObject.channels:
            if str(textChannel.type) == "text":
                print(str(textChannel.name))
                channelWriteup = ""
                messages = await textChannel.history().flatten() #fetch all messages in channel.
                m = [x.content for x in messages][::-1]  # reverse messages
                for body in m:
                    channelWriteup = channelWriteup + body + "\n"
                ## VALIDATE INPUT ## -- Messages over 1000 chars. 
                while len(channelWriteup) > 1000:
                    await embed.add_field(textChannel.name, channelWriteup[0:997])
                    channelWriteup = channelWriteup[997:]
                ## IF EMPTY, SENDING a single quote ## 
                if channelWriteup == "":
                    channelWriteup = "'" # "Cannot send empty message ERROR"
                await embed.add_field(textChannel.name, channelWriteup)
        if embed.length > 0:
            await embed.send_message()
        #else:
            #await ctx.send("This CTF has already been merged or something has gone very, very wrong :(")
        pass

def setup(bot):
    bot.add_cog(archiveCog(bot))