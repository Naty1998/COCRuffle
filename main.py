import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
import random
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

raffles = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@slash.slash(name="createraffle", description="Create a new raffle",
             options=[
                 create_option(
                     name="rafflename",
                     description="Name of the raffle",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 )
             ])
async def create_raffle(ctx: SlashContext, rafflename: str):
    if rafflename in raffles:
        await ctx.send(f"A raffle with the name {rafflename} already exists.", hidden=True)
    else:
        raffles[rafflename] = {}
        await ctx.send(f"Raffle {rafflename} created!", hidden=True)

@slash.slash(name="addparticipant", description="Add a participant to a raffle",
             options=[
                 create_option(
                     name="rafflename",
                     description="Name of the raffle",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 )
             ])
async def add_participant(ctx: SlashContext, rafflename: str):
    if rafflename not in raffles:
        await ctx.send(f"No raffle found with the name {rafflename}.", hidden=True)
        return

    modal = {
        "type": 4,
        "data": {
            "custom_id": "add_participant_modal",
            "title": "Add Participant",
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 4,
                            "custom_id": "participant_name",
                            "label": "Participant Name",
                            "style": 1,
                            "min_length": 1,
                            "max_length": 100,
                            "placeholder": "Enter participant's name",
                            "required": True
                        }
                    ]
                },
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 4,
                            "custom_id": "tickets",
                            "label": "Number of Tickets",
                            "style": 1,
                            "min_length": 1,
                            "max_length": 10,
                            "placeholder": "Enter number of tickets",
                            "required": True
                        }
                    ]
                },
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "Submit",
                            "style": ButtonStyle.green,
                            "custom_id": "submit_participant"
                        }
                    ]
                }
            ]
        }
    }

    await ctx.send("Please fill out the form to add a participant.", components=[modal])

@bot.event
async def on_socket_response(msg):
    if msg["t"] == "INTERACTION_CREATE" and msg["d"]["data"]["custom_id"] == "submit_participant":
        data = msg["d"]["data"]["components"]
        participant_name = data[0]["components"][0]["value"]
        tickets = int(data[1]["components"][0]["value"])
        rafflename = msg["d"]["message"]["components"][0]["components"][0]["value"]

        if participant_name in raffles[rafflename]:
            raffles[rafflename][participant_name] += tickets
        else:
            raffles[rafflename][participant_name] = tickets

        await bot.http.create_interaction_response(
            msg["d"]["id"],
            msg["d"]["token"],
            type=4,
            data={"content": f"Added {participant_name} with {tickets} tickets to {rafflename}."}
        )

@slash.slash(name="selectwinner", description="Select winners from a raffle",
             options=[
                 create_option(
                     name="rafflename",
                     description="Name of the raffle",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 ),
                 create_option(
                     name="numberofwinners",
                     description="Number of winners to select",
                     option_type=SlashCommandOptionType.INTEGER,
                     required=True
                 )
             ])
async def select_winner(ctx: SlashContext, rafflename: str, numberofwinners: int):
    if rafflename not in raffles:
        await ctx.send(f"No raffle found with the name {rafflename}.", hidden=True)
        return

    participants = raffles[rafflename]
    tickets_pool = [name for name, tickets in participants.items() for _ in range(tickets)]

    if len(participants) < numberofwinners:
        await ctx.send(f"Not enough participants to select {numberofwinners} winners.", hidden=True)
        return

    winners = set()
    while len(winners) < numberofwinners and len(tickets_pool) > 0:
        winner = random.choice(tickets_pool)
        winners.add(winner)
        tickets_pool = [ticket for ticket in tickets_pool if ticket != winner]

    await ctx.send(f"The winners are: {', '.join(winners)}")

bot.run(TOKEN)
