import discord
import requests
from datetime import datetime, timedelta
from discord.ext import commands
from settings import settings
from typing import Any


intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


def get_stock_value(ticker: str):
    # NOTE: Using the free tier of polygon api, we can't get latest ticker price, so we use the previous daily close
    yesterday = datetime.now() - timedelta(days=1)
    fd = yesterday.strftime('%Y-%m-%d')
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{fd}/{fd}?apiKey={settings.polygon_api_key}"
    response = requests.get(url)
    data = response.json()

    # TODO: Refactor this with proper exception handling
    try:
        stock_value = data["results"][0]["c"]
    except Exception:
        if data.get("status") == "ERROR":
            stock_value = "ratelimit"
        else:
            stock_value = None

    return stock_value


def get_msg_response(stock_value: Any, ticker: str) -> str:
    if stock_value == "ratelimit":
        msg = "Rate limit reached. Please wait one minute and try again."
    else:
        if not stock_value:
            msg = f"There was an error. Make sure {ticker} is a valid ticker."
        else:
            msg = f"{ticker} last daily close was: **${stock_value}**"
    return msg


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message: str):
    if message.author == bot.user:
        return

    if message.content.startswith('$'):
        ticker = message.content[1:].upper()
        stock_value = get_stock_value(ticker)
        msg_response = get_msg_response(stock_value, ticker)
        await message.channel.send(msg_response)
    else:
        if isinstance(message.channel, discord.DMChannel):
            instructions = (
                "Hello! You can use the $ sign followed by a ticker to get the latest stock daily close price."
                "For example, '$AAPL'."
            )
            await message.channel.send(instructions)

    await bot.process_commands(message)


# Test bot command
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')


bot.run(settings.bot_token)
