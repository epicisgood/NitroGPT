import discord
from discord.ext import commands
import openai
import asyncio

class ChatGpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        if isinstance(message.channel, discord.DMChannel):
            channel = print(f"{username} said {user_message}: in dms")
        else:
            channel = str(message.channel.name)

        try:
            if channel == "nitrogpt" or isinstance(message.channel, discord.DMChannel):
                async with message.channel.typing():  # Simulate typing status
                    response = await self.gptchat(user_message)
                    await asyncio.sleep(0.5)  # Simulate some additional processing time
                    await message.reply(response)

                    try:
                        my_message = await asyncio.wait_for(self.get_user_input(), timeout=2.5)
                        if my_message is not None:
                            await message.channel.send(my_message)
                    except asyncio.TimeoutError:
                        print("Timeout reached. No user input received.")          
        except Exception as e:
            await message.reply(str(e))

    async def gptchat(self, user_message):
        prompt = user_message
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant called NitroGPT"},
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['message']['content'].strip()

    async def get_user_input(self):
        try:
            return await asyncio.to_thread(input, "Reply to him?: ")  # Use an asynchronous input function if available
        except asyncio.CancelledError:
            pass


async def setup(bot):
    await bot.add_cog(ChatGpt(bot))