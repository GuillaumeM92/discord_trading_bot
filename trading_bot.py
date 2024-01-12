import discord
from discord.ext import commands
from settings import settings


intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')


# Run the bot with your token
bot.run(settings.bot_token)
