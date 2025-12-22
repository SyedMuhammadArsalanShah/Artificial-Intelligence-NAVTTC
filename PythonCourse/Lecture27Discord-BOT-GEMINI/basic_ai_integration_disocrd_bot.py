

import os

from dotenv import load_dotenv
from google import genai

import discord

load_dotenv()
token = os.getenv("SECRET_KEY")
token_G = os.getenv("GEMINI_API_KEY")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if client.user != message.author:
        if client.user in message.mentions:
            channel = message.channel

            # The client gets the API key from the environment variable `GEMINI_API_KEY`.
            clients = genai.Client(api_key=token_G)

            response = clients.models.generate_content(
                model="gemini-2.5-flash", contents=message.content
            )
            print(response.text)

            await channel.send(response.text)

client.run(token)
