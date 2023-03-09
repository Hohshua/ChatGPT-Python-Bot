import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

BOT_CHANNEL = 1081007925084037130
PAST_MESSAGES = 5

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')
    

message_log = []
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name == 'mart-gpt':
        async with message.channel.typing():
            message_log.append({'role': 'user', 'content': message.author.name + ': ' + message.content})
            print(message_log[-1]['role'] + ': ' + message_log[-1]['content'])
            if len(message_log) > PAST_MESSAGES:
                message_log.pop(0)
            response = openai.ChatCompletion.create(
                model = 'gpt-3.5-turbo',
                messages = message_log,
                temperature = 0.7
            )
            message_log.append({'role': 'assistant', 'content': response.choices[0].message.content})
            await message.channel.send(f'{response.choices[0].message.content}')
            print(message_log[-1]['role'] + ': ' + message_log[-1]['content'])

client.run(os.getenv('BOT_TOKEN'))