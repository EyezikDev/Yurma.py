from datetime import datetime

import discord
from discord.ext import commands

# Version (DO NOT TOUCH)
YurmaVersion = 1.2

footerMessageDefault = f"v{discord.__version__} Discord.py  •  v{YurmaVersion} YurmaBot"
botDebugChannel = 519324051701760012
embedColor = 0x8011fc


class Startup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # Debug channel for OWNER use
        botOnline = self.client.get_channel(botDebugChannel)
        # Embed for start message
        startEmbed = discord.Embed(title='Bot Online!', description=f'{round(self.client.latency * 1000)}ms',
                                   color=discord.Color(embedColor), timestamp=datetime.utcnow()) \
            .set_footer(text=f'{footerMessageDefault}') \
            .set_author(name=self.client.user, icon_url=self.client.user.avatar_url)
        # Send start message
        await botOnline.send(embed=startEmbed)
        # Set game status
        await self.client.change_presence(activity=discord.Game(name=f"y!help - On {len(self.client.guilds)} Servers"))
        # Console Log
        print(f"Bot Online : Latency {round(self.client.latency * 1000)}ms : v{YurmaVersion} YurmaBot")

    # # # # # #
    # On Stop #
    # # # # # #
    # When Bot goes offline mirror the on_ready() output.
    # Mine ping
    @commands.Cog.listener()
    async def on_disconnect(self):
        botOnline = self.client.get_channel(519324051701760012)
        endEmbed = discord.Embed(title='Bot Offline!',
                                 color=discord.Color(embedColor),
                                 timestamp=datetime.utcnow()) \
            .set_footer(text=f'')
        await botOnline.send(embed=endEmbed)


def setup(client):
    client.add_cog(Startup(client))
