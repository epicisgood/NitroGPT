import random, discord
from discord.ext import commands, bridge
from googleapiclient.discovery import build
from main import GOOGLE_API, GOOGLE_SEARCH, IMAGE_SEARCH

class Google_Search(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @bridge.bridge_command(name='generate',with_app_command=True, aliases=['image', 'gen', "image_gen"], description='Generates a random image from google', image="Type something to generate an image from google!")
  async def google_image(self, ctx, *, image: str):
    ran = random.randint(0, 9)
    google_sevice = build(
        "customsearch", "v1", developerKey=GOOGLE_API
    ).cse()
    result = google_sevice.list(
        q=f"{image}", cx=IMAGE_SEARCH, searchType="image"
    ).execute()
    out_image = result["items"][ran]["link"]
    await ctx.reply(content=out_image)

  @bridge.bridge_command(name='search',with_app_command=True, aliases=['search_engine', 'lookup'])
  async def google_search(self, ctx, *, search: str):
    google_sevice = build(
        "customsearch", "v1", developerKey=GOOGLE_API
    ).cse()
    ran = random.randint(0,2)
    result = google_sevice.list(
        q=search, cx=GOOGLE_SEARCH
    ).execute()
    url = result["items"][ran]['link']
    content = str(result["content"])
    await ctx.reply(url + "\n" + content)
    





def setup(bot):
  bot.add_cog(Google_Search(bot))
