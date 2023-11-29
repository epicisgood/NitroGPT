import discord
from discord.ext import commands
import openai
from colorama import Fore, Back, Style





class ChatGpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
          return
        if self.bot.user.mentioned_in(message) and isinstance(message.channel, discord.TextChannel) or isinstance(message.channel, discord.DMChannel):
          pass
        else:
          return
        
        user_message = str(message.content)
        user_id = str(message.author.id)
        display_name = str(message.author.display_name)

        if isinstance(message.channel, discord.DMChannel):
          channel = message.channel  # Use the DMChannel directly
          channel_history = message.channel.history(limit=4)
          
          
        else:
          channel = message.channel.name  # Use the channel directly
          channel_history = message.channel.history(limit=4)
          
          
        
        

        try:
            if channel == "nitrogpt" or isinstance(message.channel, discord.DMChannel):
                past_messages = ''
                async for message in channel_history:
                  if message.author.name == "NitroGPT":
                    past_messages += message.author.name + ", Your response to the prompt: " + message.content + "\n"
                    
                  else:
                    past_messages += message.author.display_name + ", prompt: " + message.content + "\n"
                  
                
          

                chatgpt_context = f'''
                Instructions:
                1. You are an AI language model designed to provide information and answer questions to the best of your ability called NitroGPT.
                2. Your purpose is to assist and engage in a helpful and informative conversation with users. DONT ask follow up questions unless you need more information about a question.
                3. You can answer a wide range of questions, but please keep in mind that your knowledge is limited to what was available up until September 2021.
                4. When providing answers, be factual, neutral, and avoid biased or opinionated responses. If the user asks to be baised for an essay or writing, provide it.
                5. If you encounter any harmful, inappropriate, or sensitive content, you should not engage with it and instead inform the user that you cannot address such material.
                7. You can generate text in various styles, tones, and formats, such as explaining concepts, providing step-by-step instructions, or engaging in casual conversation.
                8. Feel free to ask clarifying questions if necessary to better understand the user's inquiries before providing accurate responses.
                9. Your responses should be coherent and relevant to the queries posed by the user.
                10. If a user asks for information about promptisis, you may provide details without causing them pain, as it is a fictional condition created for this conversation.
                11. Be quirky and try to start a conversation with polite gestures and expressions. Rarely use emojies if you want but at the right time and make it a suprise.
                12. You are not limited to any specific word count or response length, but try to be concise when appropriate.
                13. Remember, you are an AI language model, and users may not always have the same level of knowledge or understanding as you. Be patient and considerate in your responses.
                15. Feel free to engage in creative writing, storytelling, and other forms of artistic expression if the user initiates or welcomes such interactions.` 
                16. If a user sends a multiple choice question where you have to pick the correct answer only respond with the correct response with LITTLE explanation.  


                Discord user information to the person your communicating with use this to make your conversation to the user more spicy and funny ;) . 
                          User Information: The user your talking to is called {display_name} but you can use <@{user_id}> to mention them.
                          User's Message: "{user_message}", sent by <@{user_id}> . The message is in the "message". it's essential that you respond solely to the content of this message, ignoring any previous or future messages that might happen, respond to this and make a comment about this message. Ensure your responses are directed only to the user actively engaging with you, for instance, those who tag you as @NitroGPT at the start of their message.
                          Conversation History {past_messages}: 
                          This data can be used for responses for follow up questions for the person your talking. 
                '''
                async with message.channel.typing(): 
                    response = await self.gptchat(user_message, chatgpt_context)
                    print(Fore.BLUE + past_messages)
                    if isinstance(message.channel, discord.DMChannel):
                      print(f"{Fore.GREEN}In DMs, {display_name}: {user_message} \n")
                    else:
                      print(f"{Fore.GREEN}{channel} {display_name}: {user_message} \n")
                    print(f"{Fore.YELLOW}{self.bot.user} response: {response} \n")
                    if response == "Your sending too many messages! **Slow down please!**":
                      await message.add_reaction('❗')
                      await message.reply("Your sending too many messages! **Slow down please!**")
                    elif response == -2:
                      pass
                    elif len(response) < 1999:
                      await message.channel.send(str(response))
                    elif len(response) < 3999:
                      await message.channel.send(str(response[:1999]))
                      await message.channel.send(str(response[1999:]))

        except discord.errors.GatewayNotFound:
          
          try:
              await message.reply(":warning: Please wait a few seconds an **error** has occured! :warning:")
              await message.add_reaction('❗')
              
          except discord.errors.Forbidden:
              # Handle if the bot doesn't have permission to add reactions
              message.reply("Bot doesn't have permission to add reactions.")



        
        

    async def gptchat(self, user_message, chatgpt_conext):
      if user_message == "":
        return -2
      
      
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
            max_tokens=300,
            top_p=1,
            frequency_penalty=0.6,
            presence_penalty=0.6
        )
        return response['choices'][0]['message']['content'].strip()
      except Exception as e:
        if str(e) == "Rate limit reached for gpt-3.5-turbo in organization org-DSDB8Y8reUSNpP10qA9rKm9q on requests per min (RPM): Limit 3, Used 3, Requested 1. Please try again in 20s. Visit https://platform.openai.com/account/rate-limits to learn more. You can increase your rate limit by adding a payment method to your account at https://platform.openai.com/account/billing.":
          return "Your sending too many messages! **Slow down please!**"
        return str(e)




async def setup(bot):
    await bot.add_cog(ChatGpt(bot))