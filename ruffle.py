import discord
import dotenv
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))
cogs_list = [
    'drawwinners',
    'checkpastruffles'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')
