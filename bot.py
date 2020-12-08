# Imports
from datetime import datetime

import os

# Test
# Version (DO NOT TOUCH)
import discord
from discord.ext import commands, menus
from pip._vendor import requests

YurmaVersion = 1.5

embedColor = 0x8011fc


# Token read from text file
def read_token():
    with open("Extra/token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


def read_key():
    with open("Extra/keys.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Token from text file
token = read_token()

# Client start then link the token and start
client = commands.Bot(command_prefix=commands.when_mentioned_or("y!"), case_insensitive=True)
client.remove_command('help')
client.owner_id(347718757105532939)


def fortnite_tracker_api_top(platform, nickname):
    url = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + nickname
    req = requests.get(url, headers={"TRN-Api-Key": "fc6a2045-846d-4f0f-bf28-b9801151e889"})
    if req.status_code == 200:
        try:
            lifetime_stats = req.json()['lifeTimeStats']
            return lifetime_stats[0:]
        except KeyError:
            return False
    else:
        return False


def fortnite_tracker_api_stats(platform, nickname):
    url = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + nickname
    req = requests.get(url, headers={"TRN-Api-Key": "fc6a2045-846d-4f0f-bf28-b9801151e889"})
    if req.status_code == 200:
        try:
            lifetime_stats = req.json()['lifeTimeStats']
            return lifetime_stats[7:]
        except KeyError:
            return False
    else:
        return False


def fortnite_map():
    url = 'https://fortnite-api.com/v1/map'
    req = requests.get(url)
    if req.status_code == 200:
        try:

            lifetime_stats = req.json()['lifeTimeStats']
            return lifetime_stats[7:]
        except KeyError:
            return False
    else:
        return False


def fortnite_avatar(platform, nickname):
    url = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + nickname
    req = requests.get(url, headers={"TRN-Api-Key": "fc6a2045-846d-4f0f-bf28-b9801151e889"})
    if req.status_code == 200:
        try:
            avatar = req.json()['avatar']
            return avatar
        except KeyError:
            return False
    else:
        return False


class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        leave_embed = discord.Embed(title=f'- Remove YurmaBot From This Server? -',
                                    description=f'> :white_check_mark: - Yes \n> :x: - No',
                                    color=discord.Color(embedColor),
                                    timestamp=datetime.utcnow())
        return await channel.send(embed=leave_embed)

    @menus.button('\N{WHITE HEAVY CHECK MARK}')
    async def on_thumbs_up(self, payload):
        leaveEmbed = discord.Embed(title=f'- Removed YurmaBot -',
                                   color=discord.Color(embedColor),
                                   timestamp=datetime.utcnow())
        await self.message.edit(embed=leaveEmbed)
        await self.message.delete(delay=3)
        await self.message.guild.leave(delay=4)

    @menus.button('\N{CROSS MARK}')
    async def on_thumbs_down(self, payload):
        await self.message.delete()


########################################################################################################################
#              #
# !!!!COGS!!!! #
#              #
################

@client.command()
async def load(extension):
    client.load_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Could Load: {filename}")
    else:
        print(f"Couldn't Load: {filename}")

client.run(token)
