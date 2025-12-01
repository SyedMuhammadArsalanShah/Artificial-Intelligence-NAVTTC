import json
import os
import numpy as np
from dotenv import load_dotenv
import discord
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from tiktoken import encoding_for_model
from openai import OpenAI
from google import genai

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
DISCORD_TOKEN = os.getenv("SECRET_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -----------------------------
# Discord client setup
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# -----------------------------
# Load posts
# -----------------------------
with open("facebook_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# -----------------------------
# Embedding utilities
# -----------------------------
enc = encoding_for_model("text-embedding-3-small")

def chunk_text(text, max_tokens=7000):
    """Split text into chunks safely under token limit."""
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunks.append(enc.decode(chunk_tokens))
    return chunks

def get_embedding_safe(text):
    """Get embeddings for all chunks of the text (no averaging)."""
    if not text.strip():
        return []  # empty text → empty list

    client = OpenAI(api_key=OPENAI_API_KEY)
    chunks = chunk_text(text)
    embeddings = []

    for chunk in chunks:
        if not chunk.strip():
            continue
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-3-small"
        )
        embeddings.append(np.array(response.data[0].embedding))

    return embeddings  # list of vectors

# -----------------------------
# Load or create embeddings
# -----------------------------
if os.path.exists("embeddings.joblib"):
    post_embeddings = joblib.load("embeddings.joblib")
    print("Embeddings loaded from file.")
else:
    print("Creating new embeddings...")
    post_embeddings = [
        {"post": p, "embeddings": get_embedding_safe(p["content"])}
        for p in posts if p["content"].strip()
    ]
    joblib.dump(post_embeddings, "embeddings.joblib")
    print("Embeddings saved to embeddings.joblib")

# -----------------------------
# Find similar post
# -----------------------------
def find_similar_post(query, top_k=1):
    query_embeddings = get_embedding_safe(query)
    if not query_embeddings:
        return []

    scores = []

    for item in post_embeddings:
        max_score = 0
        for q_emb in query_embeddings:
            for p_emb in item["embeddings"]:
                score = cosine_similarity([q_emb], [p_emb])[0][0]
                if score > max_score:
                    max_score = score
        scores.append((max_score, item["post"]))

    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[:top_k]

# -----------------------------
# Discord events
# -----------------------------
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        query = message.content
        channel = message.channel

        best_match = find_similar_post(query=query)
        if not best_match:
            await channel.send("معذرت، مجھے کوئی متعلقہ پوسٹ نہیں ملی۔")
            return

        context = "\n\n".join([p["content"] for _, p in best_match])
        prompt = f"""
Context:
{context}

Question:
{query}

Answer in Urdu naturally using the context.
"""

        # Call Gemini API
        clients = genai.Client(api_key=GEMINI_API_KEY)
        response = clients.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        await channel.send(response.text)

# -----------------------------
# Run the bot
# -----------------------------
client.run(DISCORD_TOKEN)
