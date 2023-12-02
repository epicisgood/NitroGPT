from discord.ext import commands, bridge
from main import GOOGLE_API
from googleapiclient.discovery import build



class Google_Search(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @bridge.bridge_command(name='google_search',with_app_command=True, aliases=['google', 'search'])
  async def google_search(self, ctx, *, search_inp: str):
    google_sevice = build(
        "customsearch", "v1", developerKey=GOOGLE_API
    )


def setup(bot):
  bot.add_cog(Google_Search(bot))
  