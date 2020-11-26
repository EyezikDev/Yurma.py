# Import Discord.py
import asyncio
from datetime import datetime
from discord.ext import commands

import random
import discord
from discord.ext.commands import MissingPermissions, has_permissions

YurmaVersion = 1.0


# Token read from text file
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Token from text file
token = read_token()

# Client start then link the token and start
client = commands.Bot(command_prefix="y!")

now = datetime.now()
currentTime = now.strftime("%H:%M:%S")


# When Bot goes online get the Eyezik Text server and
# Display the bot is online as well as the ping.
# Embed has a footer of discord.py version and yurmabot version.
#
# On top of this also set the Playing y!help message
@client.event
async def on_ready():
    botOnline = client.get_channel(519324051701760012)
    startEmbed = discord.Embed(
        title='Bot Online!',
        description=f'{round(client.latency * 1000)}ms',
        color=discord.Color(0x9700ff)
    )
    startEmbed.set_footer(text=f'v{discord.__version__} Discord.py  •  v{YurmaVersion} YurmaBot  •  {currentTime}')
    startEmbed.set_author(name=client.user, icon_url=client.user.avatar_url)
    await botOnline.send(embed=startEmbed)
    await client.change_presence(activity=discord.Game(name="y!help"))


# When Bot goes offline mirror the on_ready() output.
# Mine ping
@client.event
async def on_disconnect():
    botOnline = client.get_channel(519324051701760012)
    endEmbed = discord.Embed(
        title='Bot Offline!',
        color=discord.Color(0x9700ff)
    )
    endEmbed.set_footer(text=f'v{discord.__version__} Discord.py  •  v{YurmaVersion} YurmaBot  •  {currentTime}')
    await botOnline.send(embed=endEmbed)


# # # # # # # # #
# y!ping        #
# # # # # # # # #
# Sends server ping
@client.command()
async def ping(ctx):
    pingEmbed = discord.Embed(
        title='Pong Latency  🏓',
        description=f'{round(client.latency * 1000)}ms',
        color=discord.Color(0x9700ff)
    )
    pingEmbed.set_footer(text=f'v{discord.__version__} Discord.py  •  v{YurmaVersion} YurmaBot  •  {currentTime}')
    await ctx.send(embed=pingEmbed)


# # # # # # # # #
# y!roll        #
# # # # # # # # #
# Rolls a dice with 100 sides
@client.command(aliases=['dice'])
async def roll(ctx, sides):
    try:
        if 6 > sides > 100000:
            diceEmbed = discord.Embed(
                title=f'Dice roll 1 - {sides} 🎲',
                description=f'{ctx.author.mention} Rolled a **{random.randint(1, int(sides))}**',
                color=discord.Color(0x9700ff)
            )
            diceEmbed.set_footer(text=f'v{discord.__version__} Discord.py  •  v{YurmaVersion} YurmaBot  •  {currentTime}')
            await ctx.send(embed=diceEmbed)
    except:
        diceErrorEmbed = discord.Embed(
            title=f'Please Enter A Valid Number ❌',
            description='- **y!roll (Number)**\nSides must be 6 - 100,000',
            color=discord.Color(0x9700ff)
        )
        await ctx.send(embed=diceErrorEmbed)


# # # # # # # # #
# y!clear {num} #
# # # # # # # # #
# Clears specified number of messages
@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    clearEmbed = discord.Embed(
        title=f'Can Not Clear More Then 100 Messages',
        description=f'Run by {ctx.author.mention}',
        color=discord.Color(0x9700ff)
    )
    if amount > 100:
        await ctx.channel.purge(limit=1)
        await(await ctx.send(embed=clearEmbed)).delete(delay=5)
    else:
        await ctx.channel.purge(limit=+2)
        clearEmbed = discord.Embed(
            title=f'Cleared {amount} Messages',
            description=f'Run by {ctx.author.mention}',
            color=discord.Color(0x9700ff)
        )
        clearEmbed.set_footer(text=f'{ctx.guild.name}  •  v{YurmaVersion} YurmaBot  •  {currentTime}')
        await(await ctx.send(embed=clearEmbed)).delete(delay=2)
    clearEmbed = discord.Embed(
        title=f'You Do Not Have Permissions For That!',
        description=f'Run by {ctx.author.mention}',
        color=discord.Color(0x9700ff)
    )
    await(await ctx.send(embed=clearEmbed)).delete(delay=5)


client.run(token)
