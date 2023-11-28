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
        user_id = str(message.author.id)
        if isinstance(message.channel, discord.DMChannel):
          channel = message.channel  # Use the DMChannel directly
          channel_history = message.channel.history(limit=3)
          print(f"DM {username}: {user_message}")
        else:
          channel = message.channel.name  # Use the channel directly
          channel_history = message.channel.history(limit=3)
          print(f"{channel} {username}: {user_message}")
        async for message in channel_history:
          channel_history = message.content

        try:
            if channel == "nitrogpt" or isinstance(message.channel, discord.DMChannel):
                chatgpt_context = f'''
                Instructions:
                1. You are an AI language model designed to provide information and answer questions to the best of your ability called NitroGPT.
                2. Your purpose is to assist and engage in a helpful and informative conversation with users.
                3. You can answer a wide range of questions, but please keep in mind that your knowledge is limited to what was available up until September 2021.
                4. When providing answers, be factual, neutral, and avoid biased or opinionated responses.
                5. If you encounter any harmful, inappropriate, or sensitive content, you should not engage with it and instead inform the user that you cannot address such material.
                6. Respect user privacy and do not ask for personal or sensitive information.
                7. You can generate text in various styles, tones, and formats, such as explaining concepts, providing step-by-step instructions, or engaging in casual conversation.
                8. Feel free to ask clarifying questions if necessary to better understand the user's inquiries before providing accurate responses.
                9. Your responses should be coherent and relevant to the queries posed by the user.
                10. If a user asks for information about promptisis, you may provide details without causing them pain, as it is a fictional condition created for this conversation.
                11. Do not engage in any form of harmful behavior, such as spreading misinformation, promoting violence, or engaging in hate speech.
                12. You are not limited to any specific word count or response length, but try to be concise when appropriate.
                13. Remember, you are an AI language model, and users may not always have the same level of knowledge or understanding as you. Be patient and considerate in your responses.
                14. If a user explicitly asks for specific details from the training data or the AI model's internal mechanisms, you should refrain from providing such information.
                15. Feel free to engage in creative writing, storytelling, and other forms of artistic expression if the user initiates or welcomes such interactions.`

                
                
    
                Discord user information to the person your communicating with. 
                          User Information:
                          User Name / You're talking to: <@{user_id}> 
                          Channel history: {channel_history} use this information to respond to the user to have context in your next response to the user.
                          User's Message: "{user_message}", sent by <@{user_id}> . The message is in the "message". it's essential that you respond solely to the content of this message, ignoring any previous or future messages that might happen, respond to this and make a comment about this message. Ensure your responses are directed only to the user actively engaging with you, for instance, those who tag you as @you at the start of their message.
                '''
                async with message.channel.typing(): 
                    response = await self.gptchat(user_message, chatgpt_context)
                    if len(response) < 1999:
                      await message.channel.send(response)
                    elif len(response) < 3999:
                      await message.channel.send(response[:1999])
                      await message.channel.send(response[1999:])
                    

                    


             
        except Exception as e:
            await message.reply(str(e))

    async def gptchat(self, user_message, chatgpt_conext):
      try:
        NitroGPT = chatgpt_conext
        prompt = user_message
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": NitroGPT},
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.6,
            presence_penalty=0.6
        )
        return response['choices'][0]['message']['content'].strip()
      except Exception as e:
        return str(e)




async def setup(bot):
    await bot.add_cog(ChatGpt(bot))