from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions, CommandNotFound, MissingPermissions

import random
import discord

# Version (DO NOT TOUCH)

YurmaVersion = 1.2

footerMessageDefault = f"v{discord.__version__} Discord.py"
unbanDiscord = "https://discord.gg/RQwQvuAu9a"
botDebugChannel = 519324051701760012
embedColor = 0x8011fc


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    #                   #
    # !!!!BOT UTILS!!!! #
    #                   #
    #####################

    # # # # # # # # #
    # y!ping        #
    # # # # # # # # #
    # Sends bot ping
    @commands.command()
    async def ping(self, ctx):
        # Delete command message
        await ctx.channel.purge(limit=1)
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        pingPics = ["https://media.tenor.com/images/3f3ab14069ecd0df6153ad94ed6695fc/tenor.gif",
                    "https://media1.tenor.com/images/5ed009f22ae0ea4090586adb91462a47/tenor.gif",
                    "https://media1.tenor.com/images/2b27c6e7747d319f76fd98d2a226ab33/tenor.gif"]
        choice = random.choice(pingPics)
        # Ping Embed
        pingEmbed = discord.Embed(title='Pong Latency  🏓',
                                  description=f'{round(self.client.latency * 1000)}ms',
                                  color=discord.Color(embedColor),
                                  timestamp=datetime.utcnow()) \
            .set_footer(text=f"Command Run By {ctx.author}",
                        icon_url=f"{ctx.author.avatar_url}") \
            .set_thumbnail(url=choice)
        # Send Embed
        await ctx.send(embed=pingEmbed)

    @commands.command(aliases=['userinfo', 'info'])
    async def user(self, ctx):
        # Delete command message
        await ctx.channel.purge(limit=1)
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Check if there was a mentioned user
        # Otherwise get the author
        if not ctx.message.mentions:
            member = ctx.author
        else:
            member = ctx.message.mentions[0]
        # Get Members roles
        roleList = []
        separator = ', '
        for role in member.roles[1:]:
            roleList.append(role.mention)
        # Reverse the list so the top role is first
        roleList.reverse()
        userEmbed = discord.Embed(color=discord.Color(embedColor),
                                  timestamp=datetime.utcnow()) \
            .add_field(name="Server Nickname:", value=f"{member.display_name}", inline=False) \
            .add_field(name="Account Id:", value=member.id, inline=False) \
            .add_field(name="Account Creation Date:", value=member.created_at.strftime("%b. %d %Y - %I:%M %p"),
                       inline=False) \
            .add_field(name="Join Server Date:", value=member.joined_at.strftime("%b. %d %Y - %H:%M %p"),
                       inline=False) \
            .add_field(name="Account Roles:", value=f"{separator.join(roleList)}", inline=False) \
            .add_field(name="Profile Picture:", value=f"[Here]({member.avatar_url})", inline=False) \
            .set_author(name=f"{member}'s information", icon_url=member.avatar_url) \
            .set_footer(text=f"Command Run By {ctx.author}",
                        icon_url=f"{ctx.author.avatar_url}")
        # Send Embed
        await ctx.send(embed=userEmbed)

    ####################################################################################################################
    #                   #
    # !!!!BOT GAMES!!!! #
    #                   #
    #####################

    # # # # # # # # #
    # y!roll        #
    # # # # # # # # #
    # Rolls a dice with 6-100000 sides
    @commands.command(aliases=['dice'])
    async def roll(self, ctx, sides):
        # Delete command message
        await ctx.channel.purge(limit=1)
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Try...
        try:
            # If sides in between 6 and 100,000
            if 6 <= int(sides) <= 100000:
                # Dice Embed
                diceEmbed = discord.Embed(title=f'Dice roll 1 - {sides} 🎲',
                                          description=f'\n{ctx.author.mention} '
                                                      f'Rolled a **{random.randint(1, int(sides))}**',
                                          color=discord.Color(embedColor),
                                          timestamp=datetime.utcnow()) \
                    .set_footer(text=f"Command Run By {ctx.author}",
                                icon_url=f"{ctx.author.avatar_url}") \
                    .set_thumbnail(url="https://media1.tenor.com/images/b05ce342004baef013060d72f95a378f/tenor.gif")
                # Send Embed
                await ctx.send(embed=diceEmbed)
            # Else the number is Invalid
            else:
                # Dice Error Embed
                diceErrorEmbed = discord.Embed(title=f'Please Enter A Valid Number ❌',
                                               description='- Sides must be 6 - 100,000.',
                                               color=discord.Color(embedColor),
                                               timestamp=datetime.utcnow()) \
                    .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
                # Send Embed
                await ctx.send(embed=diceErrorEmbed, delete_after=10)
        # Catch...
        except:
            # Dice Error 2 Embed
            # If the user input isn't a int tell users
            diceErrorEmbed = discord.Embed(title=f'Please Enter A Valid Number ❌',
                                           description='- Sides Must Be a Number.',
                                           color=discord.Color(embedColor),
                                           timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            # Send Embed
            await ctx.send(embed=diceErrorEmbed, delete_after=10)

    ####################################################################################################################
    #                        #
    # !!!!STAFF COMMANDS!!!! #
    #                        #
    ##########################

    # # # # # # # # #
    # y!clear {num} #
    # # # # # # # # #
    # Clears specified number of messages
    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        # Delete command message
        await ctx.channel.purge(limit=1)
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # If amount of lines to clear is under 100
        if amount <= 100:
            # Clear Embed
            clearEmbed = discord.Embed(title=f'Cleared {amount} Messages',
                                       color=discord.Color(embedColor),
                                       timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            # Purge Chat
            await ctx.channel.purge(limit=amount)
            # Send Embed
            await ctx.send(embed=clearEmbed, delete_after=2)
        # Else
        else:
            # Clear Error Embed
            clearErrorEmbed = discord.Embed(title=f'Can Not Clear More Then 100 Messages',
                                            color=discord.Color(embedColor),
                                            timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            # Send Embed
            await ctx.send(embed=clearErrorEmbed, delete_after=5)

    # # # # # # # # # # # # #
    # y!kick {user} {reason}#
    # # # # # # # # # # # # #
    # Kick user with a reason
    @commands.command()
    # Has Permission to kick user
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        # Delete command message
        await ctx.channel.purge(limit=1)
        # Gifs for embed, pick at random
        kickPics = ["https://media1.tenor.com/images/2ce5a017f6556ff103bce87b273b89b7/tenor.gif",
                    "https://media1.tenor.com/images/d54f63dd2f5f807f6de4eedb48ca949b/tenor.gif",
                    "https://media1.tenor.com/images/4dd99934237218f35c02b7cbf4ac9f9f/tenor.gif",
                    "https://media1.tenor.com/images/cc217519af48fe13bea6004afb36f1f2/tenor.gif"]
        choice = random.choice(kickPics)
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Kick Embed
        kickEmbed = discord.Embed(title=f"Kicked ***{member}*** 👟",
                                  description=f'Reason: {reason}',
                                  color=discord.Color(embedColor),
                                  timestamp=datetime.utcnow()) \
            .set_thumbnail(url=choice) \
            .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        # Make a invite
        invite = await ctx.channel.create_invite()
        # You Kick Embed
        youKickEmbed = discord.Embed(
            title=f'Kicked From {ctx.guild.name} 👟',
            description=f"Kicked by {ctx.author.mention}\n\n"
                        f"You are able to join back, but your roles are removed.\n"
                        f"In the future please avoid breaking the rules.\n"
                        f'To join back use the link [Here!]({invite})',
            color=discord.Color(embedColor),
            timestamp=datetime.utcnow()
        ) \
            .set_author(name=ctx.guild.name,
                        icon_url=f"https://cdn.discordapp.com/icons/{ctx.guild.id}/{ctx.guild.icon}.png") \
            .set_image(url=choice)
        # Send Embeds
        await ctx.send(embed=kickEmbed)
        await ctx.send(embed=kickEmbed, delete_after=5)
        await member.send(embed=youKickEmbed)
        # Kick
        await member.kick(reason=reason)

    # # # # # # # # # # # # #
    # y!ban {user} {reason} #
    # # # # # # # # # # # # #
    # Ban user with a reason
    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        # Delete command message
        await ctx.channel.purge(limit=1)
        # Gifs for embed, pick at random
        banPics = ["https://media1.tenor.com/images/885cdbb1e6950cefdc981db000079c85/tenor.gif",
                   "https://media1.tenor.com/images/380b96c755c9d0855a784c8f51e1515f/tenor.gif",
                   "https://media1.tenor.com/images/380b96c755c9d0855a784c8f51e1515f/tenor.gif"]
        choice = random.choice(banPics)
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Ban Embed
        banEmbed = discord.Embed(title=f"Banned ***{member}*** 🔨",
                                 description=f'Reason: {reason}',
                                 color=discord.Color(embedColor),
                                 timestamp=datetime.utcnow()) \
            .set_thumbnail(url=choice) \
            .set_footer(text=f"Command Run By {ctx.author}",
                        icon_url=f"{ctx.author.avatar_url}")
        # You Ban Embed
        youBanEmbed = discord.Embed(
            title=f'Banned From {ctx.guild.name} 👟',
            description=f"Banned by {ctx.author.mention} for ***reason: {reason}***\n"
                        f"In the future please avoid breaking the rules and please comply with staff.\n\n"
                        f"Want to be notified if you ever get unbanned? Join [This Discord]({unbanDiscord})! "
                        f"This allows Yurma to communicate with you in the future.",
            color=discord.Color(embedColor),
            timestamp=datetime.utcnow()
        ) \
            .set_image(url=choice) \
            .set_author(name=ctx.guild.name,
                        icon_url=f"https://cdn.discordapp.com/icons/{ctx.guild.id}/{ctx.guild.icon}.png")
        # Send Embeds
        await member.send(embed=youBanEmbed)
        await ctx.send(embed=banEmbed)
        await ctx.send(embed=banEmbed, delete_after=10)
        # Ban
        await member.ban(reason=reason)

    # # # # # # # # # # # # #
    # y!pardon,unban {user} #
    # # # # # # # # # # # # #
    # Unbans User
    @commands.command(aliases=['pardon'])
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        # Delete command message
        await ctx.channel.purge(limit=1)
        # Console Log
        print(f"{ctx.author} executed {ctx.command} : Unbanning {member}")
        # Grab the list of banned users in the server
        bannedUser = await ctx.guild.bans()
        # If that list is empty...
        if not bannedUser:
            # Console Log
            print(f"{ctx.guild.name}'s Banlist is Empty : No Unban")
            # Make Embed
            unbanEmbed = discord.Embed(title=f'No One Is Banned.',
                                       color=discord.Color(embedColor),
                                       timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            # Display embed for 5 secs.
            await ctx.send(embed=unbanEmbed, delete_after=5)
        # Else...
        else:
            # Try to...
            try:
                # Split the staff defined user at the members '#' Ex. Isaac#1234 = Isaac 1234
                memberName, memberNum = member.split('#')
                # Unban Embed
                unbanEmbed = discord.Embed(title=f'Unbanned ***{member}*** 👼',
                                           description=f'Unbanned by {ctx.author.mention}',
                                           color=discord.Color(embedColor),
                                           timestamp=datetime.utcnow()) \
                    .set_thumbnail(url="https://media1.tenor.com/images/fb1aa76944c156acc494fff37ebdbcfa/tenor.gif") \
                    .set_footer(text=f"Command Run By {ctx.author}",
                                icon_url=f"{ctx.author.avatar_url}")
                # For amount of bans in the ban list
                for ban_entry in bannedUser:
                    # Current ban entry
                    user = ban_entry.user
                    # If the split name equals the current ban entry
                    if (user.name, user.discriminator) == (memberName, memberNum):
                        # That is the user, unban them
                        await ctx.guild.unban(user)
                        # Console Log
                        print(f"Unban {user} successful")
                        # Send Embed
                        await ctx.send(embed=unbanEmbed)
                        await ctx.send(embed=unbanEmbed, delete_after=10)
                        # Invite back to server
                        invite = await ctx.channel.create_invite()
                        # You Unban Embed
                        youUnbanEmbed = discord.Embed(
                            title=f'Unbanned From {ctx.guild.name} 👼',
                            description=f'Unbanned by {ctx.author.mention}\n\n'
                                        f'You are able to join back, but your roles are removed and you are being '
                                        f'watched.In the future please avoid breaking the rules and please comply '
                                        f'with staff. To join back use the link [Here!]({invite})',
                            color=discord.Color(embedColor),
                            timestamp=datetime.utcnow()
                        ) \
                            .set_author(name=ctx.guild.name,
                                        icon_url=f"https://cdn.discordapp.com/icons/"
                                                 f"{ctx.guild.id}/{ctx.guild.icon}.png") \
                            .set_image(url="https://media1.tenor.com/images"
                                           "/fb1aa76944c156acc494fff37ebdbcfa/tenor.gif")
                        # Try...
                        try:
                            # To send the embed to user
                            await user.send(embed=youUnbanEmbed)
                        # If they aren't in another server with YurmaBot the message will error and not send
                        # So skip it and continue
                        except:
                            return
            # If you can't split the defined user...
            except:
                # Console Log
                print(f"{member} Can Not Be Unbanned")
                # Unban Embed
                unbanEmbed = discord.Embed(title=f'{member} Isn''t A Valid User ❌',
                                           color=discord.Color(embedColor),
                                           timestamp=datetime.utcnow()) \
                    .set_footer(text=f"Command Run By {ctx.author}",
                                icon_url=f"{ctx.author.avatar_url}")
                # Send Embed
                await ctx.send(embed=unbanEmbed, delete_after=5)

    # # # # # # # # # #
    # y!banlist,bans  #
    # # # # # # # # # #
    # Shows Server Ban Users
    @commands.command(aliases=['bans'])
    @has_permissions(ban_members=True)
    async def banlist(self, ctx):
        # Delete command message
        await ctx.channel.purge(limit=1)
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Grab the list of banned users in the server
        bannedUsers = await ctx.guild.bans()
        # If the list of banned users if empty then...
        if not bannedUsers:
            # Console Log
            print(f"{ctx.guild.name}'s Banlist is Empty : No Output")
            # Banlist Embed
            banlistEmbed = discord.Embed(title=f'Banlist Empty',
                                         color=discord.Color(embedColor),
                                         timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            # Send Embed
            await ctx.send(embed=banlistEmbed, delete_after=5)
        # Else...
        else:
            # Console Log
            print(f"{ctx.guild.name}'s Banlist Has User(s) : Output")
            # Banlist Embed
            banlistEmbed = discord.Embed(title=f'Banned Users In {ctx.guild.name} :notepad_spiral:',
                                         color=discord.Color(embedColor),
                                         timestamp=datetime.utcnow())\
                .set_thumbnail(url=ctx.guild.icon_url) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            # For amount of bans in the ban list
            for ban_entry in bannedUsers:
                # Current ban entry
                user = ban_entry.user
                banlistEmbed.add_field(name=f'\n{user}', value=f'Reason: {ban_entry.reason}\n', inline=False)
            # Send Embed
            await ctx.send(embed=banlistEmbed)

    ####################################################################################################################
    #                    #
    # !!!!BOT ERRORS!!!! #
    #                    #
    ######################

    # # # # # # # #
    # Clear Error #
    # # # # # # # #
    # Error if no perms
    @commands.Cog.listener()
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            noPermEmbed = discord.Embed(title=f'You Do Not Have Perms To Clear Chat ❌',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=noPermEmbed, delete_after=5)

    # # # # # # # #
    # Kick Error  #
    # # # # # # # #
    # Error if no perms
    @commands.Cog.listener()
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            noPermEmbed = discord.Embed(title=f'You Do Not Have Perms To Kick ❌',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=noPermEmbed, delete_after=5)

    # # # # # # #
    # Ban Error #
    # # # # # # #
    # Error if no perms
    @commands.Cog.listener()
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            noPermEmbed = discord.Embed(title=f'You Do Not Have Perms To Ban ❌',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=noPermEmbed, delete_after=5)

    # # # # # # # #
    # Unban Error #
    # # # # # # # #
    # Error if no perms
    @commands.Cog.listener()
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            noPermEmbed = discord.Embed(title=f'You Do Not Have Perms To Unban ❌',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=noPermEmbed, delete_after=5)

    # # # # # # # # #
    # Banlist Error #
    # # # # # # # # #
    # Error if no perms
    @commands.Cog.listener()
    @banlist.error
    async def banlist_error(self, ctx, error):
        await ctx.channel.purge(limit=1)
        if isinstance(error, MissingPermissions):
            noPermEmbed = discord.Embed(title=f'You Do Not Have Perms To Check The Banlist ❌',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=noPermEmbed, delete_after=5)

    # # # # # # # # #
    # Not a command #
    # # # # # # # # #
    # Tell user that what they typed isn't a command
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            notCmdEmbed = discord.Embed(title=f'Not a command ❌',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=notCmdEmbed, delete_after=3)

    ####################################################################################################################
    #               #
    # !!!!EXTRA!!!! #
    #               #
    #################

    # # # # # # # # #
    # Emmy Command#
    # # # # # # # # #
    @commands.command()
    async def emmy(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        if ctx.author.id == 318794495502188545 or 347718757105532939:
            emmyEmbed = discord.Embed(description=f"**Shut the Fuck Up** {member.mention}",
                                      color=discord.Color(embedColor)) \
                .set_image(url="https://media1.tenor.com/images/cf00b4b51e95dc81781ce5992c2f1f05/tenor.gif") \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=emmyEmbed)
        else:
            eyezikEmbed = discord.Embed(title='Your Not Emmy',
                                        color=discord.Color(embedColor))
            await ctx.send(embed=eyezikEmbed, delete_after=3)

    # # # # # # # # #
    # Eyezik Command#
    # # # # # # # # #
    @commands.command()
    async def fuckyou(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        if ctx.author.id == 347718757105532939:
            eyezikEmbed = discord.Embed(title=f"",
                                        description=f'**Frick you** {member.mention}',
                                        color=discord.Color(embedColor)) \
                .set_image(url="https://media.discordapp.net/attachments/722702340620288042/752701313514471644/tenor_"
                               "-_2020-09-08T112610.001.gif") \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            await ctx.send(embed=eyezikEmbed)
        else:
            eyezikEmbed = discord.Embed(title='Your Not Eyezik',
                                        color=discord.Color(embedColor))
            await ctx.send(embed=eyezikEmbed, delete_after=3)


def setup(client):
    client.add_cog(Commands(client))
