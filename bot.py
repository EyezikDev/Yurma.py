# Imports
from discord.ext import commands

import os

# Test
# Version (DO NOT TOUCH)
from pip._vendor import requests

YurmaVersion = 1.5


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


def fortnite_tracker_api_top(platform, nickname):
    URL = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + nickname
    req = requests.get(URL, headers={"TRN-Api-Key": "fc6a2045-846d-4f0f-bf28-b9801151e889"})
    if req.status_code == 200:
        try:
            lifetime_stats = req.json()['lifeTimeStats']
            return lifetime_stats[0:]
        except KeyError:
            return False
    else:
        return False


def fortnite_tracker_api_stats(platform, nickname):
    URL = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + nickname
    req = requests.get(URL, headers={"TRN-Api-Key": "fc6a2045-846d-4f0f-bf28-b9801151e889"})
    if req.status_code == 200:
        try:
            lifetime_stats = req.json()['lifeTimeStats']
            return lifetime_stats[7:]
        except KeyError:
            return False
    else:
        return False


def fortnite_map():
    URL = 'https://fortnite-api.com/v1/map'
    req = requests.get(URL)
    if req.status_code == 200:
        try:

            lifetime_stats = req.json()['lifeTimeStats']
            return lifetime_stats[7:]
        except KeyError:
            return False
    else:
        return False


def fortnite_avatar(platform, nickname):
    URL = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + nickname
    req = requests.get(URL, headers={"TRN-Api-Key": "fc6a2045-846d-4f0f-bf28-b9801151e889"})
    if req.status_code == 200:
        try:
            avatar = req.json()['avatar']
            return avatar
        except KeyError:
            return False
    else:
        return False


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
