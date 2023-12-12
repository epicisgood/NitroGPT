import discord
from discord.ext import commands
import openai
from colorama import Fore





class ChatGpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conversation_history = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
          return
        
        if self.bot.user.mentioned_in(message) or "bb" in message.content[0:5].lower() or "nitro" in message.content.lower() or isinstance(message.channel, discord.DMChannel):
          pass
        else:
          return
        
        user_message = str(message.content)
        user_id = str(message.author.id)
        display_name = str(message.author.display_name)

        if user_id not in self.conversation_history:
          self.conversation_history[user_id] = []
          
        self.conversation_history[user_id].append({
            "author_name": message.author.name,
            "display_name": message.author.display_name,
            "content": message.content
        })

        self.conversation_history[user_id] = self.conversation_history[user_id]

        if isinstance(message.channel, discord.DMChannel):
          channel = message.channel  # Use the DMChannel directly
          
        
          
        else:
          channel = message.channel.name  # Use the channel directly
          

        
          
        try:
            if channel == "ai-chat" or isinstance(message.channel, discord.DMChannel):
                def format_conversation_history(self, history):
                  formatted_history = ""
                  for msg in history:
                      formatted_history += f"{msg['author_name']} ({msg['display_name']}): {msg['content']}\n"
                  return formatted_history
                
    
                chatgpt_context = f'''
                Instructions:
                Be a freindly bot that intereact with the user in a funny, dark humor, or energetic. You can use emojies to express your feelings.
                If the user asks for an essay dont use swear words in that essay.
                if the user sends multiple choice questions for example: which of the following is correct: This, that, other, 4th. Only answer with the correct answer and with a short one sentence response.

                Make sure to interact like a normal discord user, dont be asking for questions like "how can  i assist you today" or any of that nonsense. just answer the question you were ask and end it there.
                User Information: The user your talking to is called {display_name} but you can use <@{user_id}> to mention them.
                User's Message: "{user_message}", sent by <@{user_id}> . The message is in the "message". it's essential that you respond solely to the content of this message, ignoring any previous or future messages that might happen, respond to this and make a comment about this message. Ensure your responses are directed only to the user actively engaging with you, for instance, those who tag you as <@1177390053002059796> at the start of their message.
                Conversation History: {format_conversation_history(self, self.conversation_history[user_id])}: 
                This data can be used for responses for follow up questions for the person your talking. 
                '''
                origin_message = await message.channel.fetch_message(message.id)
                await origin_message.add_reaction("✅")
                async with message.channel.typing():
                  response = await self.gptchat(user_message, chatgpt_context)
                  
                  if response == "Your sending too many messages! **Slow down please!**":
                          await origin_message.remove_reaction("✅", self.bot.user)
                          await origin_message.add_reaction('❌')
                          await origin_message.reply("Your sending too many messages! **Slow down please!**")
                  

                  
                  if isinstance(message.channel, discord.DMChannel):
                    print(f"{Fore.LIGHTGREEN_EX}In DMs, {display_name}: {user_message} \n")
                  else:
                    print(f"{Fore.LIGHTGREEN_EX}{channel} {display_name}: {user_message} \n")
                  print(f"{Fore.LIGHTYELLOW_EX}{self.bot.user} response: {response} \n")
                    

                    
                  if response == -2:
                      pass
                  elif len(response) < 1999:
                    await origin_message.reply(str(response[:1999]))
                  elif len(response) < 3999:
                    await message.channel.send(str(response[:1999]))
                    await message.channel.send(str(response[1999:]))

        except discord.errors.GatewayNotFound:
          
          try:
              origin_message = await message.channel.fetch_message(message.id)
              await origin_message.reply(":warning: Please wait a few seconds an **error** has occured! :warning:")
              await origin_message.add_reaction('⚠️')
              
          except discord.errors.Forbidden:
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
            max_tokens=256,
            top_p=1,
            frequency_penalty=0.6,
            presence_penalty=0.6
        )
        return response['choices'][0]['message']['content'].strip()
      except Exception as e:
        if str(e) == "Rate limit reached for gpt-3.5-turbo in organization org-DSDB8Y8reUSNpP10qA9rKm9q on requests per min (RPM): Limit 3, Used 3, Requested 1. Please try again in 20s. Visit https://platform.openai.com/account/rate-limits to learn more. You can increase your rate limit by adding a payment method to your account at https://platform.openai.com/account/billing.":
          return "Your sending too many messages! **Slow down please!**"
        return str(e)




def setup(bot):
  bot.add_cog(ChatGpt(bot))