# mega_ai_discord_bot.py – Full One-File Version
from bs4 import BeautifulSoup
import json, os, numpy as np, joblib, discord
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from tiktoken import encoding_for_model
from openai import OpenAI
from google import genai

# Environment
load_dotenv()
DISCORD_TOKEN = os.getenv("SECRET_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Scrape
with open("fbpost.html", "r", encoding="utf-8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")
posts = [
    {"post": i, "content": p.get_text(strip=True)}
    for i, p in enumerate(soup.find_all("div", class_="_2pin"), start=1)
]
with open("facebook_posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

# Embeddings
enc = encoding_for_model("text-embedding-3-small")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def chunk_text(text, max_tokens=7000):
    tokens = enc.encode(text)
    return [
        enc.decode(tokens[i : i + max_tokens])
        for i in range(0, len(tokens), max_tokens)
    ]


def get_embeddings(text):
    return [
        np.array(
            openai_client.embeddings.create(input=chunk, model="text-embedding-3-small")
            .data[0]
            .embedding
        )
        for chunk in chunk_text(text)
    ]


if os.path.exists("embeddings.joblib"):
    post_embeddings = joblib.load("embeddings.joblib")
else:
    post_embeddings = [
        {"post": p, "embeddings": get_embeddings(p["content"])} for p in posts
    ]
    joblib.dump(post_embeddings, "embeddings.joblib")


# Similarity
def find_best_post(query):
    query_embeddings = get_embeddings(query)
    best_score, best_post = 0, None
    for item in post_embeddings:
        for q in query_embeddings:
            for p in item["embeddings"]:
                score = cosine_similarity([q], [p])[0][0]
                if score > best_score:
                    best_score, best_post = score, item["post"]
    return best_post


# Discord Bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user in message.mentions:
        query = message.content
        post = find_best_post(query)
        if not post:
            await message.channel.send("معذرت، کوئی متعلقہ پوسٹ نہیں ملی.")
            return
        prompt = f"Context:\n{post['content']}\n\nQuestion:\n{query}\n\nAnswer in simple Urdu."
        gemini = genai.Client(api_key=GEMINI_API_KEY)
        response = gemini.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        await message.channel.send(response.text)


client.run(DISCORD_TOKEN)
