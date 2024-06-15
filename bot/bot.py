import discord
import os
from config.config import BOT_TOKEN

bot = discord.Bot()

cogs_list = [
    'greetings',
    'checkpastruffles',
    'drawwinners'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

bot.run(BOT_TOKEN)
