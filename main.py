import discord
from discord.ext import commands, tasks
import youtube_dl
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
with open('key.txt', 'r') as read:
    api_key = read.readline()
    read.close()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='No possible motivation me',
    intents=intents)


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
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

@bot.command(name = 'join')
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name = 'leave')
async def leave(ctx):
    await ctx.guild.voice_client.disconnect()
    await ctx.send('Im leave')

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queue = []
        self.is_playing = False

    async def play_next(self, ctx):
        while len(self.music_queue > 0):
            url = self.music_queue[0][0]['source']
            self.music_queue.pop[0]
            self.is_playing = True
            Music.play(ctx, url)

    @commands.command(name = 'play')
    async def play(self, ctx, url):
        voice_channel = ctx.author.voice.channel

        if self.is_playing == True:
            await ctx.send('Added to queue')
            self.music_queue.append([url, voice_channel])
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: self.play_next())

        await ctx.send(f'Now playing: {player.title}')  

    @commands.command(name = 'pause')
    async def pause(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        await ctx.send("paused")
        await voice_channel.pause()

    @commands.command(name = 'resume')
    async def resume(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client
        await ctx.send("resume")
        await voice_channel.resume()

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

bot.add_cog(Music(bot))
bot.run(api_key)