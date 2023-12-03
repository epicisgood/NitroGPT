import discord
from discord.ext import bridge
import openai
from colorama import Fore
import os

openai.api_key = os.environ["OPENAI"]
DISCORD_TOKEN = os.environ['DISCORD']
GOOGLE_API = os.environ['GOOGLE_API']
GOOGLE_SEARCH = os.environ['GOOGLE_SEARCH']
IMAGE_SEARCH = os.environ['IMAGE_SEARCH']


intents = discord.Intents.all()
bot = bridge.Bot(command_prefix='a?', intents=intents)



@bot.event
async def on_ready():
    print(f'{Fore.LIGHTBLUE_EX}We have logged in as {Fore.LIGHTMAGENTA_EX}{bot.user} \n')
    
bot.load_extensions("chatgpt", "google_search")



bot.remove_command("help")




bot.run(DISCORD_TOKEN)
