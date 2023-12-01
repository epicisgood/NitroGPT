import discord
from discord.ext import commands, bridge


class Google_Search(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @bridge.bridge_command(name='google_search',with_app_command=True, aliases=['google', 'search'])
  async def google_search(self, ctx, *, search_inp: str):
    test = await ctx.reply(search_inp)
    ori_ctx = await test.original_response()
    await ori_ctx.add_reaction("🥣")
   


def setup(bot):
  bot.add_cog(Google_Search(bot))
  