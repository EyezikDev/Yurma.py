import asyncio

import discord
import youtube_dl
from discord import ClientException
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

queue = []

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return

        else:
            channel = ctx.message.author.voice.channel

        await channel.connect()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def play(self, ctx, url):
        global queue

        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return

        else:
            channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
        except ClientException:
            pass

        server = ctx.message.guild
        voice_channel = server.voice_client
        queue.append(url)
        await ctx.send(f'`{url}` added to queue!')

        player = await YTDLSource.from_url(queue[0], loop=self.client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('**Now playing:** {}'.format(player.title))

    @commands.Cog.listener()
    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            try:
                server = ctx.message.guild
                voice_channel = server.voice_client
                player = await YTDLSource.from_url(queue[0], loop=self.client.loop)
                voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send('**Now playing:** {}'.format(player.title))
                del (queue[0])
            except IndexError:
                await ctx.send("please add a song")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remove(self, ctx, number):
        try:
            del (queue[int(number)])
            await ctx.send(f'Your queue is now `{queue}!`')
        except IndexError:
            await ctx.send('Your queue is either **empty** or you need to enter a valid number')

    @commands.command(aliases=['q'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def queue(self, ctx):
        await ctx.send(f'Your queue is now `{queue}!`')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stop(self, ctx):
        try:
            await ctx.channel.purge(limit=1)
        except discord.errors.Forbidden:
            pass
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.leave()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pause(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.pause()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def resume(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        voice_channel.resume()


def setup(client):
    client.add_cog(Music(client))
