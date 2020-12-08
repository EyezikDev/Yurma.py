import os
import sys
import traceback
from datetime import datetime

from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from pip._vendor import requests
from bot import fortnite_tracker_api_top, fortnite_tracker_api_stats, fortnite_avatar, read_key, MyMenu

import random
import discord

# Version (DO NOT TOUCH)

YurmaVersion = 1.5

footerMessageDefault = f"v{discord.__version__} Discord.py"
unbanDiscord = "https://discord.gg/RQwQvuAu9a"
botDebugChannel = 519324051701760012
embedColor = 0x8011fc

helpUntTitle = "Utility Commands :gear:"
helpUnt = "\n > **y!help** - Pulls up this menu\n" \
          " > **y!invite** - Invite YurmaBot to your own server\n" \
          " > **y!ping** - Current bot ping\n" \
          " > **y!user** - Shows your account information\n" \
          " > **y!user {mention}** - Shows mentioned accounts information\n" \
          " > **y!facts** - Facts command help menu\n" \
          " > **y!search {phrase}** - Built in search engine\n" \
          " > **y!fortnite** - Fortnite command help menu\n"

helpFunTitle = "Fun Commands :gem:"
helpFun = "\n > **y!roll {number}** - Rolls a dice \n> *(More then 6, less then 100,000)*\n"

helpModTitle = "Moderation Commands :crossed_swords:"
helpMod = "\n> **y!joinmessage** - Information on setting up user join message TODO\n" \
          "> **y!leavemessage** - Information on setting up leave join message TODO\n" \
          "> **y!clear {number}** - Clears a number of lines in chat. \n> *(Default 10, Max 50)*\n" \
          "> **y!kick {mention} {reason}** - Kicks mentioned user\n" \
          "> **y!ban {mention} {reason}** - Bans mentioned user\n" \
          "> **y!unban {name#1234}** - Unbans user\n" \
          "> **y!banlist** - Shows banned users of the server\n" \
          "> **y!leave** - Safe way to remove YurmaBot"
helpFortniteTitle = "Epic Games Stats :chart_with_upwards_trend: "
helpFortnite = "\n> **y!fortnite os {platform} {name}** - Overall Stats\n" \
               "> **y!fortnite ps {platform} {name}** - Placement Stats\n"

helpFactsTitle = "Type of Facts :globe_with_meridians:"
helpFacts = "\n> **y!fact random** - Quick random fact\n" \
            "> **y!fact animals {animal}** - Quick fact of a animal\n"


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def restart(self, ctx):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        if ctx.author.id == 347718757105532939:
            # Console Log
            print(f"{ctx.author} executed {ctx.command}")
            restartEmbed = discord.Embed(title='~~──────────~~ Restarting ~~───────────~~',
                                         color=discord.Color(embedColor),
                                         timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            # Send Embed
            await ctx.send(embed=restartEmbed)
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            # Console Log
            print(f"{ctx.author} executed {ctx.command}, but it did nothing")

    ####################################################################################################################
    #                   #
    # !!!!BOT UTILS!!!! #
    #                   #
    #####################

    # # # # # #
    # y!help  #
    # # # # # #
    # Command help
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Ping Embed
        helpEmbed = discord.Embed(title='~~──────────────~~ Help ~~──────────────~~',
                                  description=f'Full Documentation of commands [here TODO]'
                                              f'(https://www.eyezik.net/yurmabot/docs)',
                                  color=discord.Color(embedColor),
                                  timestamp=datetime.utcnow()) \
            .add_field(name=helpUntTitle, value=helpUnt, inline=False) \
            .add_field(name=helpFunTitle, value=helpFun, inline=False) \
            .add_field(name=helpModTitle, value=helpMod, inline=False) \
            .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}") \
            .set_thumbnail(url=ctx.bot.user.avatar_url)
        # Send Embed
        await ctx.send(embed=helpEmbed)

    # # # # # # #
    # y!invite  #
    # # # # # # #
    # Invite YurmaBot to your discord
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def invite(self, ctx):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Ping Embed
        inviteEmbed = discord.Embed(title='~~────────────~~ Invite ~~─────────────~~',
                                    description=f'YurmaBot invite link [here!]'
                                                f'(https://discord.com/api/oauth2/authorize?client_id='
                                                f'781139148249497610&permissions=1342663799&scope=bot)',
                                    color=discord.Color(embedColor),
                                    timestamp=datetime.utcnow()) \
            .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}") \
            # Send Embed
        await ctx.send(embed=inviteEmbed)

    # # # # # #
    # y!ping  #
    # # # # # #
    # Sends bot ping
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        pingPics = ["https://media.tenor.com/images/3f3ab14069ecd0df6153ad94ed6695fc/tenor.gif",
                    "https://media1.tenor.com/images/5ed009f22ae0ea4090586adb91462a47/tenor.gif",
                    "https://media1.tenor.com/images/2b27c6e7747d319f76fd98d2a226ab33/tenor.gif"]
        choice = random.choice(pingPics)
        # Ping Embed
        pingEmbed = discord.Embed(title='~~──────────~~ Latency  🏓 ~~──────────~~',
                                  description=f'{round(self.client.latency * 1000)}ms',
                                  color=discord.Color(embedColor),
                                  timestamp=datetime.utcnow()) \
            .set_footer(text=f"Command Run By {ctx.author}",
                        icon_url=f"{ctx.author.avatar_url}") \
            .set_thumbnail(url=choice)
        # Send Embed
        await ctx.send(embed=pingEmbed)

    # # # # # #
    # y!user  #
    # # # # # #
    # User information based on server
    @commands.command(aliases=['userinfo', 'info'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def user(self, ctx):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
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
        userEmbed = discord.Embed(title="~~───────────~~ User Info ~~───────────~~",
                                  color=discord.Color(embedColor),
                                  timestamp=datetime.utcnow()) \
            .add_field(name="Server Nickname:", value=f"{member.display_name}", inline=False) \
            .add_field(name="Account Id:", value=member.id, inline=False) \
            .add_field(name="Account Creation Date:", value=member.created_at.strftime("%b. %d %Y - %I:%M %p"),
                       inline=False) \
            .add_field(name="Account Server Join Date:", value=member.joined_at.strftime("%b. %d %Y - %H:%M %p"),
                       inline=False) \
            .add_field(name="Account Roles:", value=f"{separator.join(roleList)}", inline=False) \
            .add_field(name="Profile Picture:", value=f"[Here]({member.avatar_url})", inline=False) \
            .set_author(name=f"{member}'s information", icon_url=member.avatar_url) \
            .set_footer(text=f"Command Run By {ctx.author}",
                        icon_url=f"{ctx.author.avatar_url}")
        # Send Embed
        await ctx.send(embed=userEmbed)

    # # # # # # # # #
    # y!facts       #
    # # # # # # # # #
    # Fact command help
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def facts(self, ctx):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        fortniteEmbed = discord.Embed(title='~~────────────~~ Facts ~~────────────~~',
                                      color=discord.Color(embedColor),
                                      timestamp=datetime.utcnow()) \
            .add_field(name=helpFactsTitle, value=helpFacts, inline=False) \
            .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}") \
            .set_thumbnail(url=ctx.bot.user.avatar_url)
        # Send Embed
        await ctx.send(embed=fortniteEmbed)

    # # # # # # # # # # # #
    # y!facts random      #
    # # # # # # # # # # # #
    # Random Fact (BROKEN)
    @facts.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def random(self, ctx):
        fact = ""
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        URL = f"https://uselessfacts.jsph.pl/random.json?language=en"
        REQ = requests.get(URL, headers={})
        if REQ.status_code == 200:
            fact = REQ.json()['text']
        else:
            await ctx.send(f"API returned a {REQ.status}.")
        randomEmbed = discord.Embed(title=f'~~──────────~~ Random Fact ~~───────────~~',
                                    description=f'> {fact}',
                                    color=discord.Color(embedColor),
                                    timestamp=datetime.utcnow()) \
            .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=randomEmbed)

    # # # # # # # # # # # #
    # y!facts animals     #
    # # # # # # # # # # # #
    # Animal Fact
    @facts.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def animals(self, ctx, animal):
        fact, link = "", ""
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        animals = ["dog", "cat", "fox", "panda", "bird", "koala"]
        if animal in animals:
            URL = f"https://some-random-api.ml/facts/{animal}"
            IMG = f"https://some-random-api.ml/img/{animal}"
            REQ = requests.get(URL, headers={})
            REQIMG = requests.get(IMG, headers={})
            if REQ.status_code == 200:
                fact = REQ.json()['fact']
            else:
                await ctx.send(f"API returned a {REQ.status}.")
            if REQIMG.status_code == 200:
                link = REQIMG.json()['link']
            else:
                await ctx.send(f"API returned a {REQ.status}.")

            animalEmbed = discord.Embed(title=f'~~───────────~~ {animal.capitalize()} Fact ~~───────────~~',
                                        description=f'> {fact}',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}") \
                .set_thumbnail(url=link)
            await ctx.send(embed=animalEmbed)
        else:
            separator = ', '
            animalEmbed = discord.Embed(title=f'Not a valid animal ❌',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .add_field(name="Animal List", value=f"> {separator.join(animals)}", inline=False) \
                .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            # Purge Chat
            await ctx.send(embed=animalEmbed)

    # # # # # # # # #
    # y!search      #
    # # # # # # # # #
    # Search Engine
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def search(self, ctx, *, google):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")

        searchTerm = google.replace(" ", "+")
        url = "https://bing-web-search1.p.rapidapi.com/search"
        querystring = {"q": f"{searchTerm}", "mkt": "en-us", "textFormat": "Raw", "safeSearch": "Strict",
                       "freshness": "Day",
                       "answerCount": "3"}
        headers = {
            'x-bingapis-sdk': "true",
            'x-rapidapi-key': f"{read_key()}",
            'x-rapidapi-host': "bing-web-search1.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        search = response.json()['queryContext']['originalQuery']
        URL = f"https://www.google.com/search?q={search}"
        googleEmbed = discord.Embed(title=f'~~──────────────────~~ Google ~~───────────────────~~',
                                    description=f'Result for: **[{google}]({URL})**',
                                    color=discord.Color(embedColor),
                                    timestamp=datetime.utcnow()) \
            .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        for i in range(0, 3):
            googleEmbed.add_field(name=f"────────────────────────────────────────────────",
                                  value=f"**[{response.json()['webPages']['value'][i]['name']}]"
                                        f"({response.json()['webPages']['value'][i]['url']})**\n"
                                        f"{response.json()['webPages']['value'][i]['snippet']}", inline=False)
        googleEmbed.add_field(name=f"────────────────────────────────────────────────",
                              value=f"For more results check [here]({URL})", inline=False)
        # Send Embed
        await ctx.send(embed=googleEmbed)

    # # # # # # # # #
    # y!fortnite    #
    # # # # # # # # #
    # Fortnite command help
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fortnite(self, ctx):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Ping Embed
        fortniteEmbed = discord.Embed(title='~~─────────────~~ Fortnite ~~─────────────~~',
                                      description=f'Full Documentation of commands [here TODO]'
                                                  f'(https://www.eyezik.net/yurmabot/docs)',
                                      color=discord.Color(embedColor),
                                      timestamp=datetime.utcnow()) \
            .add_field(name=helpFortniteTitle, value=helpFortnite, inline=False) \
            .add_field(name="Season Info:", value="TEst", inline=False) \
            .add_field(name="Item Shop", value="Test", inline=False) \
            .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}") \
            .set_thumbnail(url=ctx.bot.user.avatar_url)
        # Send Embed
        await ctx.send(embed=fortniteEmbed)

    # # # # # # # # # # #
    # y!fortnite os     #
    # # # # # # # # # # #
    # Fortnite overall stats
    @fortnite.group()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def os(self, ctx, platform, nickname):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Ping Embed
        if platform not in ('pc', 'xbl', 'psn'):
            await ctx.send("error")
            return
        else:
            res = fortnite_tracker_api_stats(platform, nickname)
            avatar = fortnite_avatar(platform, nickname)
            if res:
                matches_played = res[0]['value']
                wins = res[1]['value']
                win_percent = res[2]['value']
                kills = res[3]['value']
                kd = res[4]['value']
                fortniteEmbed = discord.Embed(title=f"- Lifetime Stats for {nickname} - ",
                                              color=discord.Color(embedColor),
                                              timestamp=datetime.utcnow()) \
                    .add_field(name="Matches Played", value=f"> {matches_played}\n", inline=False) \
                    .add_field(name="Wins", value=f"> {wins}\n", inline=False) \
                    .add_field(name="Win percent", value=f"> {win_percent}" + '\n', inline=False) \
                    .add_field(name="Kills", value=f"> {kills}" + '\n', inline=False) \
                    .add_field(name="K/D", value=f"> {kd}" + '\n', inline=False) \
                    .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}") \
                    .set_thumbnail(url=avatar)
                await ctx.send(embed=fortniteEmbed)
            else:
                await ctx.send('Failed to get data. Double check spelling of your nickname.')

    # # # # # # # # # # #
    # y!fortnite ps     #
    # # # # # # # # # # #
    # Fortnite placements stats
    @fortnite.group()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ps(self, ctx, platform, nickname):
        if platform not in ('pc', 'xbl', 'psn'):
            await ctx.send("error")
            return
        else:
            res = fortnite_tracker_api_top(platform, nickname)
            avatar = fortnite_avatar(platform, nickname)
            if res:
                top3 = res[0]['value']
                top5 = res[1]['value']
                top6 = res[2]['value']
                top10 = res[3]['value']
                top12 = res[4]['value']
                top25 = res[5]['value']
                fortniteEmbed = discord.Embed(title="- Lifetime Stats for -" + nickname,
                                              color=discord.Color(embedColor),
                                              timestamp=datetime.utcnow()) \
                    .add_field(name="Solos:", value=f"> **Top 3's**\n> {top3}\n"
                                                    f"> **Top 5's**\n> {top5}\n", inline=False) \
                    .add_field(name="Duos:", value=f"> **Top 6's**\n> {top6}\n"
                                                   f"> **Top 10's**\n> {top10}\n", inline=False) \
                    .add_field(name="Squads:", value=f"> **Top 12's**\n> {top12}\n"
                                                     f"> **Top 25's**\n> {top25}\n", inline=False) \
                    .set_footer(text=f"Command Run By {ctx.author}", icon_url=f"{ctx.author.avatar_url}") \
                    .set_thumbnail(url=avatar)
                await ctx.send(embed=fortniteEmbed)
            else:
                await ctx.send('Failed to get data. Double check spelling of your nickname.')

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
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def roll(self, ctx, sides):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
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
        except TypeError:
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
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # If amount of lines to clear is under 100
        if amount <= 25:
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
            clearErrorEmbed = discord.Embed(title=f'Can Not Clear More Then 50 Messages',
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
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
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
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
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
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
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
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
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
                                         timestamp=datetime.utcnow()) \
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

    # # # # # # #
    # y!leave   #
    # # # # # # #
    # Kick bot but safe
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @has_permissions(kick_members=True)
    async def leave(self, ctx):
        # Delete command message
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        # Console Log
        print(f"{ctx.author} executed {ctx.command}")
        # Ping Embed
        m = MyMenu()
        await m.start(ctx)

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
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
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
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
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
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
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
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
            await ctx.send(embed=noPermEmbed, delete_after=5)

    # # # # # # # # #
    # Banlist Error #
    # # # # # # # # #
    # Error if no perms
    @commands.Cog.listener()
    @banlist.error
    async def banlist_error(self, ctx, error):
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        if isinstance(error, MissingPermissions):
            noPermEmbed = discord.Embed(title=f'You Do Not Have Perms To Check The Banlist ❌',
                                        color=discord.Color(embedColor),
                                        timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
            await ctx.send(embed=noPermEmbed, delete_after=5)

    # # # # # # # # #
    # Not a command #
    # # # # # # # # #
    # Tell user that what they typed isn't a command
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            errorEmbed = discord.Embed(title=f'Not a command ❌',
                                       description="> y!help - for a list of commands",
                                       color=discord.Color(embedColor),
                                       timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
            await ctx.send(embed=errorEmbed, delete_after=3)

        elif isinstance(error, commands.CommandOnCooldown):
            errorEmbed = discord.Embed(title=f'Command on cool down ❌',
                                       color=discord.Color(embedColor),
                                       timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
            await ctx.send(embed=errorEmbed, delete_after=1)
        elif isinstance(error, commands.TooManyArguments):
            errorEmbed = discord.Embed(title=f'Too Many Arguments ❌',
                                       color=discord.Color(embedColor),
                                       timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
            await ctx.send(embed=errorEmbed, delete_after=1)
        elif isinstance(error, commands.BotMissingPermissions):
            errorEmbed = discord.Embed(title=f'Please Insure YurmaBot Has Correct Permissions.',
                                       color=discord.Color(embedColor),
                                       timestamp=datetime.utcnow()) \
                .set_footer(text=f"Command Run By {ctx.author}",
                            icon_url=f"{ctx.author.avatar_url}")
            try:
                await ctx.channel.purge(limit=1)
            except discord.errors.Forbidden:
                pass
            await ctx.send(embed=errorEmbed, delete_after=1)

        else:
            print(''.join(traceback.format_exception(type(error), error, error.__traceback__)))

    ####################################################################################################################
    #               #
    # !!!!EXTRA!!!! #
    #               #
    #################
    # # # # # # # #
    # Emmy Command#
    # # # # # # # #
    @commands.command()
    async def emmy(self, ctx, member: discord.Member):
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
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

    # # # # # # # # # #
    # Eyezik Commands #
    # # # # # # # # # #
    @commands.command()
    async def frickyou(self, ctx, member: discord.Member = None):
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
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

    @commands.command()
    async def no(self, ctx, *, message="No"):
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        if ctx.author.id == 347718757105532939:
            await ctx.send(f"""``` 
⠀








                                                      
                                                     {message}.









⠀```""")
        else:
            eyezikEmbed = discord.Embed(title='Your Not Eyezik',
                                        color=discord.Color(embedColor))
            await ctx.send(embed=eyezikEmbed, delete_after=3)


def setup(client):
    client.add_cog(Commands(client))
