import discord
from dotenv import load_dotenv
import os
from similarity_search import find_similar_post
from google import genai

load_dotenv()
DISCORD_TOKEN = os.getenv("SECRET_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"✅ Bot logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user in message.mentions:
        query = message.content
        post = find_similar_post(query)
        if not post:
            await message.channel.send("معذرت، کوئی متعلقہ پوسٹ نہیں ملی۔")
            return

        prompt = f"""
Context:
{post['content']}

Question:
{query}

Answer in simple Urdu.
"""
        gemini = genai.Client(api_key=GEMINI_API_KEY)
        response = gemini.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        await message.channel.send(response.text)


client.run(DISCORD_TOKEN)
