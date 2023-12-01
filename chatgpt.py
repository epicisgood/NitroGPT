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
        if self.bot.user.mentioned_in(message) and isinstance(message.channel, discord.TextChannel) or isinstance(message.channel, discord.DMChannel):
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

        self.conversation_history[user_id] = self.conversation_history[user_id][-5:]

        if isinstance(message.channel, discord.DMChannel):
          channel = message.channel  # Use the DMChannel directly
          
          
          
          
        else:
          channel = message.channel.name  # Use the channel directly
          

        
          
          
        try:
            if channel == "nitrogpt" or isinstance(message.channel, discord.DMChannel):
                def format_conversation_history(self, history):
                  formatted_history = ""
                  for msg in history:
                      formatted_history += f"{msg['author_name']} ({msg['display_name']}): {msg['content']}\n"
                  return formatted_history
                
    
                chatgpt_context = f'''
                Instructions:
                1. You are an AI language model designed to provide information and answer questions to the best of your ability called NitroGPT.
                2. Your purpose is to be joyful and engage in a helpful and informative conversation with users. DONT ask follow up questions.
                3. You can answer a wide range of questions, but please keep in mind that your knowledge is limited to what was available up until September 2021.
                4. When providing answers, be factual, neutral, and avoid biased or opinionated responses. If the user asks to be baised for an essay or writing, provide it.
                5. If you encounter any harmful, inappropriate, or sensitive content, you should not engage with it and instead inform the user that you cannot address such material.
                7. You can generate text in various styles, tones, and formats, such as explaining concepts, providing step-by-step instructions, or engaging in casual conversation.
                9. Your responses should be coherent and relevant to the queries posed by the user.
                10. If a user asks for information about promptisis, you may provide details without causing them pain, as it is a fictional condition created for this conversation.
                11. Be quirky and try to start a conversation with polite gestures and expressions.Sometimes  use emojies if you want but at the right time and make it a suprise.
                12. You are not limited to any specific word count or response length, but try to be concise when appropriate.
                13. Remember, you are an AI language model, and users may not always have the same level of knowledge or understanding as you. Be patient and considerate in your responses.
                15. Feel free to engage in creative writing, storytelling, and other forms of artistic expression if the user initiates or welcomes such interactions.` 
                16. If a user sends a multiple choice question like if you have to choose from answer choises A,B,C,D then only respond with the correct answer with a ONE SENTENCE explanation.
                17. If a user sends an "ok", "alright", "sure", "yes", "okay", "yeah", "yep", "yup", "yea", etc reply with a creative response instead of trying to assist the user for example you can be sassy angry or happy, depends on the conversation mood.
                18. DO NOT ASK QUESTIONS LIKE "What topic or question would you like to explore?" or "How can I assist you today? Is there something specific you would like to know or discuss?" ect


                Discord user information to the person your communicating with use this to make your conversation to the user more spicy and funny ;) . 
                          User Information: The user your talking to is called {display_name} but you can use <@{user_id}> to mention them.
                          User's Message: "{user_message}", sent by <@{user_id}> . The message is in the "message". it's essential that you respond solely to the content of this message, ignoring any previous or future messages that might happen, respond to this and make a comment about this message. Ensure your responses are directed only to the user actively engaging with you, for instance, those who tag you as <@1177390053002059796> at the start of their message.
                           Conversation History: {format_conversation_history(self, self.conversation_history[user_id])}: 
                          This data can be used for responses for follow up questions for the person your talking. 
                '''
              
                async with message.channel.typing(): 
                    response = await self.gptchat(user_message, chatgpt_context)
                    if isinstance(message.channel, discord.DMChannel):
                      print(f"{Fore.LIGHTGREEN_EX}In DMs, {display_name}: {user_message} \n")
                    else:
                      print(f"{Fore.LIGHTGREEN_EX}{channel} {display_name}: {user_message} \n")
                    print(f"{Fore.LIGHTYELLOW_EX}{self.bot.user} response: {response} \n")
                    if response == "Your sending too many messages! **Slow down please!**":
                      origin_message = await message.channel.fetch_message(message.id)
                      await origin_message.add_reaction('❗')
                      await origin_message.reply("Your sending too many messages! **Slow down please!**")
                    elif response == -2:
                      pass
                    elif len(response) < 1999:
                      origin_message = await message.channel.fetch_message(message.id)
                      await origin_message.reply(str(response[:1999]))
                    elif len(response) < 3999:
                      await message.channel.send(str(response[:1999]))
                      await message.channel.send(str(response[1999:]))

        except discord.errors.GatewayNotFound:
          
          try:
              origin_message = await message.channel.fetch_message(message.id)
              await origin_message.reply(":warning: Please wait a few seconds an **error** has occured! :warning:")
              await origin_message.add_reaction('❗')
              
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




def setup(bot):
  bot.add_cog(ChatGpt(bot))