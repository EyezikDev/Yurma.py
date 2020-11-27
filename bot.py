# Imports
from datetime import datetime
from discord.ext import commands

import random
import discord
from discord.ext.commands import MissingPermissions, has_permissions, CommandNotFound

# Version (DO NOT TOUCH)
YurmaVersion = 1.2


# Token read from text file
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Token from text file
token = read_token()

# Client start then link the token and start
client = commands.Bot(command_prefix="y!", case_insensitive=True)

botDebugChannel = 519324051701760012
footerMessageDefault = f"v{discord.__version__} Discord.py  •  v{YurmaVersion} YurmaBot"


# # # # # #
# On Start#
# # # # # #
# When Bot goes online get the Eyezik Text server and
# Display the bot is online as well as the ping.
# Embed has a footer of discord.py version and yurmabot version.
#
# On top of this also set the Playing y!help message
@client.event
async def on_ready():
    # Debug channel for OWNER use
    botOnline = client.get_channel(botDebugChannel)
    # Embed for start message
    startEmbed = discord.Embed(title='Bot Online!', description=f'{round(client.latency * 1000)}ms',
                               color=discord.Color(0x9700ff), timestamp=datetime.now()) \
        .set_footer(text=f'{footerMessageDefault}') \
        .set_author(name=client.user, icon_url=client.user.avatar_url)
    # Send start message
    await botOnline.send(embed=startEmbed)
    # Set game status
    await client.change_presence(activity=discord.Game(name="y!help"))
    # Console Log
    print(f"Bot Online : Latency {round(client.latency * 1000)}ms : v{YurmaVersion} YurmaBot")


# # # # # #
# On Stop #
# # # # # #
# When Bot goes offline mirror the on_ready() output.
# Mine ping
@client.event
async def on_disconnect():
    botOnline = client.get_channel(botDebugChannel)
    endEmbed = discord.Embed(
        title='Bot Offline!',
        color=discord.Color(0x9700ff),
        timestamp=datetime.now()
    )
    endEmbed.set_footer(text=f'')
    await botOnline.send(embed=endEmbed)


########################################################################################################################
#                   #
# !!!!BOT UTILS!!!! #
#                   #
#####################


# # # # # # # # #
# y!ping        #
# # # # # # # # #
# Sends bot ping
@client.command()
async def ping(ctx):
    await ctx.channel.purge(limit=1)
    print(f"{ctx.author} executed {ctx.command}")
    pingEmbed = discord.Embed(
        title='Pong Latency  🏓',
        description=f'{round(client.latency * 1000)}ms',
        color=discord.Color(0x9700ff),
        timestamp=datetime.now()
    ).set_footer(text=footerMessageDefault)
    await ctx.send(embed=pingEmbed)


########################################################################################################################
#                   #
# !!!!BOT GAMES!!!! #
#                   #
#####################


# # # # # # # # #
# y!roll        #
# # # # # # # # #
# Rolls a dice with 6-100000 sides
@client.command(aliases=['dice'])
async def roll(ctx, sides):
    await ctx.channel.purge(limit=1)
    print(f"{ctx.author} executed {ctx.command}")
    try:
        if 6 <= int(sides) <= 100000:
            diceEmbed = discord.Embed(
                title=f'Dice roll 1 - {sides} 🎲',
                description=f'{ctx.author.mention} Rolled a **{random.randint(1, int(sides))}**',
                color=discord.Color(0x9700ff),
                timestamp=datetime.now()
            )
            diceEmbed.set_footer(
                text=f'{ctx.guild.name}  •  v{YurmaVersion} YurmaBot')
            await ctx.send(embed=diceEmbed)
        else:
            diceErrorEmbed = discord.Embed(
                title=f'Please Enter A Valid Number ❌',
                description='- Sides must be 6 - 100,000.',
                color=discord.Color(0x9700ff),
                timestamp=datetime.now()
            )
            await ctx.send(embed=diceErrorEmbed)
    except:
        diceErrorEmbed = discord.Embed(
            title=f'Please Enter A Valid Number ❌',
            description='- Sides Must Be a Number.',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await ctx.send(embed=diceErrorEmbed)


########################################################################################################################
#                        #
# !!!!STAFF COMMANDS!!!! #
#                        #
##########################


# # # # # # # # #
# y!clear {num} #
# # # # # # # # #
# Clears specified number of messages
@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=1)
    print(f"{ctx.author} executed {ctx.command}")
    if amount > 100:
        clearEmbed = discord.Embed(
            title=f'Can Not Clear More Then 100 Messages',
            description=f'Run by {ctx.author.mention}',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await(await ctx.send(embed=clearEmbed)).delete(delay=5)
    else:
        clearEmbed = discord.Embed(
            title=f'Cleared {amount} Messages',
            description=f'Run by {ctx.author.mention}',
            color=discord.Color(0x9700ff),
            timestamp=datetime.utcnow()
        )
        clearEmbed.set_footer(text=f'{ctx.guild.name}  •  v{YurmaVersion} YurmaBot')
        await ctx.channel.purge(limit=amount + 1)
        await(await ctx.send(embed=clearEmbed)).delete(delay=2)


# # # # # # # # # # # # #
# y!kick {user} {reason}#
# # # # # # # # # # # # #
# Kick user with a reason
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    print(f"{ctx.author} executed {ctx.command}")
    kickEmbed = discord.Embed(
        title=f'Kicked {member}',
        description=f'Run by {ctx.author.mention}  |   Reason: {reason}',
        color=discord.Color(0x9700ff),
        timestamp=datetime.now()
    )
    kickEmbed.set_footer(text=f'{ctx.guild.name}  •  v{YurmaVersion} YurmaBot')
    await(await ctx.send(embed=kickEmbed)).delete(delay=5)
    await member.kick(reason=reason)


# # # # # # # # # # # # #
# y!ban {user} {reason} #
# # # # # # # # # # # # #
# Ban user with a reason
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    print(f"{ctx.author} executed {ctx.command}")
    banEmbed = discord.Embed(
        title=f'Banned {member} 🔨',
        description=f'Run by {ctx.author.mention}  |   Reason: {reason}',
        color=discord.Color(0x9700ff),
        timestamp=datetime.now()
    )
    banEmbed.set_footer(text=f'{ctx.guild.name}  •  v{YurmaVersion} YurmaBot')
    await(await ctx.send(embed=banEmbed)).delete(delay=5)
    await member.ban(reason=reason)


# # # # # # # # # # # # #
# y!pardon,unban {user} #
# # # # # # # # # # # # #
# Unbans User
@client.command(aliases=['pardon'])
@has_permissions(ban_members=True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)
    # Console Log
    print(f"{ctx.author} executed {ctx.command} : Unbanning {member}")
    # Grab the list of banned users in the server
    bannedUser = await ctx.guild.bans()
    # If that list is empty..
    if not bannedUser:
        # Console Log
        print(f"{ctx.guild.name}'s Banlist is Empty : No Unban")
        # Make Embed
        unbanEmbed = discord.Embed(
            title=f'No One Is Banned.',
            description=f'Run by {ctx.author.mention}',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        # Display embed for 5 secs.
        await(await ctx.send(embed=unbanEmbed)).delete(delay=5)
    else:
        try:
            memberName, memberNum = member.split('#')
            for ban_entry in bannedUser:
                user = ban_entry.user
                if (user.name, user.discriminator) == (memberName, memberNum):
                    unbanEmbed = discord.Embed(
                        title=f'Unbanned ***{member}*** 👼',
                        description=f'Unbanned by {ctx.author.mention}',
                        color=discord.Color(0x9700ff),
                        timestamp=datetime.now()
                    )
                    await ctx.guild.unban(user)
                    invite = await ctx.channel.create_invite()
                    youUnbanEmbed = discord.Embed(
                        title=f'Unbanned From {ctx.guild.name} 👼',
                        description=f'Unbanned by {ctx.author.mention}\n'
                                    f'To join back use the link [Here!]({invite})',
                        color=discord.Color(0x9700ff),
                        timestamp=datetime.now()
                    )\
                        .set_author(name=ctx.guild.name,
                                    icon_url=f"https://cdn.discordapp.com/icons/{ctx.guild.id}/{ctx.guild.icon}.png")
                    await user.send(embed=youUnbanEmbed)
                    print(f"Unban {user} successful")
                    break
                else:
                    raise Exception("not real")
            await(await ctx.send(embed=unbanEmbed)).delete(delay=5)
        except:
            print(f"{member} Can Not Be Unbanned")
            unbanEmbed = discord.Embed(
                title=f'{member} Isn''t A Valid User ❌',
                description=f'Run by {ctx.author.mention}',
                color=discord.Color(0x9700ff),
                timestamp=datetime.now()
            )
            await(await ctx.send(embed=unbanEmbed)).delete(delay=5)


@client.command()
@has_permissions(ban_members=True)
async def banlist(ctx):
    await ctx.channel.purge(limit=1)
    print(f"{ctx.author} executed {ctx.command}")
    bannedUsers = await ctx.guild.bans()
    if not bannedUsers:
        print(f"{ctx.guild.name}'s Banlist is Empty : No Output")
        unbanEmbed = discord.Embed(
            title=f'Banlist Empty',
            description=f'Run by {ctx.author.mention}',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await(await ctx.send(embed=unbanEmbed)).delete(delay=5)
    else:
        print(f"{ctx.guild.name}'s Banlist Has User(s) : Output")
        banlistEmbed = discord.Embed(
            title=f'Banned Users In {ctx.guild.name}',
            description=f'Run by {ctx.author.mention}',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        for ban_entry in bannedUsers:
            user = ban_entry.user
            banlistEmbed.add_field(name=f'\n{user}', value=f'Reason: {ban_entry.reason}\n', inline=True)
        await ctx.send(embed=banlistEmbed)


########################################################################################################################
#                    #
# !!!!BOT ERRORS!!!! #
#                    #
######################


# # # # # # # #
# Clear Error #
# # # # # # # #
# Error if no perms
@client.event
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.purge(limit=1)
        noPermEmbed = discord.Embed(
            title=f'You Do Not Have Perms To Clear Chat ❌',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await(await ctx.send(embed=noPermEmbed)).delete(delay=5)


# # # # # # # #
# Kick Error  #
# # # # # # # #
# Error if no perms
@client.event
@kick.error
async def kick_error(ctx, error):
    await ctx.channel.purge(limit=1)
    if isinstance(error, MissingPermissions):
        noPermEmbed = discord.Embed(
            title=f'You Do Not Have Perms To Kick ❌',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await(await ctx.send(embed=noPermEmbed)).delete(delay=5)


# # # # # # #
# Ban Error #
# # # # # # #
# Error if no perms
@client.event
@ban.error
async def ban_error(ctx, error):
    await ctx.channel.purge(limit=1)
    if isinstance(error, MissingPermissions):
        noPermEmbed = discord.Embed(
            title=f'You Do Not Have Perms To Ban ❌',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await(await ctx.send(embed=noPermEmbed)).delete(delay=5)


# # # # # # # #
# Unban Error #
# # # # # # # #
# Error if no perms
@client.event
@unban.error
async def unban_error(ctx, error):
    await ctx.channel.purge(limit=1)
    if isinstance(error, MissingPermissions):
        noPermEmbed = discord.Embed(
            title=f'You Do Not Have Perms To Unban ❌',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await(await ctx.send(embed=noPermEmbed)).delete(delay=5)


# # # # # # # # #
# Banlist Error #
# # # # # # # # #
# Error if no perms
@client.event
@banlist.error
async def banlist_error(ctx, error):
    await ctx.channel.purge(limit=1)
    if isinstance(error, MissingPermissions):
        noPermEmbed = discord.Embed(
            title=f'You Do Not Have Perms To Check The Banlist ❌',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await ctx.channel.purge(limit=1)
        await(await ctx.send(embed=noPermEmbed)).delete(delay=5)


# # # # # # # # #
# Not a command #
# # # # # # # # #
# Tell user that what they typed isn't a command
@client.event
async def on_command_error(ctx, error):
    await ctx.channel.purge(limit=1)
    if isinstance(error, CommandNotFound):
        notCmdEmbed = discord.Embed(
            title=f'Not a command ❌',
            color=discord.Color(0x9700ff),
            timestamp=datetime.now()
        )
        await(await ctx.send(embed=notCmdEmbed)).delete(delay=3)
    else:
        return


########################################################################################################################
#              #
# !!!!COGS!!!! #
#              #
################

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


client.run(token)
