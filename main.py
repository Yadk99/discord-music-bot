from http import client
import discord
from discord.ext import commands, tasks
import nacl

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name = 'join')
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name = 'leave')
async def leave(ctx):
    await ctx.guild.voice_client.disconnect()
    await ctx.send('Im leave')

bot.run('MTAzMDUwNzg4NDU4NjQ3MTQzNg.G6TaNQ.wwSGRrgP8oeRLWW7dZ1qEKiNM40MFjuB4viHgY')