import discord
from discord.ext import commands
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI")
DISCORD_TOKEN = os.environ['DISCORD']

# Initialize the Discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)


@bot.event
async def on_ready():
    synced = len(await bot.tree.sync())
    print(f'We have logged in as {bot.user}, synced {synced} commands')
    await bot.load_extension("chatgpt")


bot.remove_command("help")




    


# Run the Discord bot
bot.run(DISCORD_TOKEN)
