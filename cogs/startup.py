from datetime import datetime
from discord.ext import commands

import discord

# Version (DO NOT TOUCH)
from bot import version

YurmaVersion = version()

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
        startEmbed = discord.Embed(title='~~──────────~~ Bot Online! ~~──────────~~',
                                   color=discord.Color(embedColor),
                                   timestamp=datetime.utcnow()) \
            .add_field(name="Ping 🏓", value=f"> {round(self.client.latency * 1000)}ms", inline=False) \
            .add_field(name="Start Time :alarm_clock:", value=f"> {datetime.utcnow().strftime('%c')}", inline=False) \
            .add_field(name="YurmaBot Version <:YurmaBot:785238144235864094>", value=f"> v{YurmaVersion}",
                       inline=False) \
            .add_field(name="Discord.py Version <:Discordpy:785235018103783474>", value=f"> v{discord.__version__}",
                       inline=False) \
            .add_field(name="Python Version <:Python:785237022382096455>", value=f"> v3.9",
                       inline=False) \
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
    # @commands.Cog.listener()
    # async def on_disconnect(self):
    #    botOnline = self.client.get_channel(519324051701760012)
    #    endEmbed = discord.Embed(title='Bot Offline!',
    #                             color=discord.Color(embedColor),
    #                             timestamp=datetime.utcnow()) \
    #        .set_footer(text=f'')
    #    await botOnline.send(embed=endEmbed)


def setup(client):
    client.add_cog(Startup(client))
