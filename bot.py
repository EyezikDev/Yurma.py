# Imports
from discord.ext import commands

import os
# Test
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
client = commands.Bot(command_prefix=commands.when_mentioned_or("y!"), case_insensitive=True)
client.remove_command('help')

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
