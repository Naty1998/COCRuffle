import discord
from discord.ext import commands

class Greetings(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @discord.slash_command() # application command
    async def hello(self, ctx: discord.ApplicationContext): 
        await ctx.respond('Hello!')

    @discord.slash_command() # application command
    async def goodbye(self, ctx: discord.ApplicationContext):
        await ctx.respond('Goodbye!')

    @discord.user_command()
    async def greet(self, ctx, member: discord.Member):
        await ctx.respond(f'{ctx.author.mention} says hello to {member.mention}!')

    math = discord.SlashCommandGroup("math", "Spooky math stuff") # create a Slash Command Group called "math"
    advanced_math = math.create_subgroup(
        "advanced",
        "super hard math commands!"
    )

    @math.command()
    async def add(self, ctx: discord.ApplicationContext, a: int, b: int):
        c = a + b
        await ctx.respond(f"{a} + {b} is {c}.")
    
    @advanced_math.command()
    async def midpoint(self, ctx: discord.ApplicationContext, x1: float, y1: float, x2: float, y2: float):
        mid_x = (x1 + x2)/2
        mid_y = (y1 + y2)/2
        await ctx.respond(f"The midpoint between those coordinates is ({mid_x}, {mid_y}).")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Greetings(bot)) # add the cog to the bot