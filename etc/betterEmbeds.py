import discord
import discord.ext
import datetime


async def sendEmbed(ctx, title, value):
        embed = discord.Embed(title="`#"+title+"`", description=value, color=0xA292C1)
        #embed.set_thumbnail(url="https://media.discordapp.net/attachments/670811518480416779/690258379951570972/logo_4.jpg")
        embed.set_author(name="**She11Sh0ck**", icon_url="https://media.discordapp.net/attachments/670811518480416779/690272290721890344/logo.jpg.png")
        embed.timestamp = datetime.datetime.utcnow()
        #embed.add_field(name=title, value=value)

        await ctx.channel.send(embed=embed)
        