import json
import os

from dotenv import load_dotenv
from google import genai

import discord
import joblib
import requests
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
token = os.getenv("SECRET_KEY")
token_G = os.getenv("GEMINI_API_KEY")
token_open = os.getenv("OPENAI_API_KEY")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# step 01 Load Data

with open("facebook_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)


# step 02 is embeddings
def get_embedding(text):
    # r = requests.post(
    #     "http://localhost:11434/api/embed",
    #     json={
    #         "model": "bge-m3",
    #         "input": [text]
    #     }
    # )
    # data = r.json()

    from openai import OpenAI

    client = OpenAI(api_key=token_open)

    response = client.embeddings.create(input=text, model="text-embedding-3-small")

    print(response.data[0].embedding)
    return np.array(response.data[0].embedding)


if os.path.exists("embeddings.joblib"):
    post_embeddings = joblib.load("embeddings.joblib")
    print("Embeddings Loaded")
else:
    print("Creatings new embeddings ")
    post_embeddings = [
        {"post": p, "embeddings": get_embedding(p["content"])} for p in posts
    ]
    joblib.dump(post_embeddings, "embeddings.joblib")
    print("JOblib embeddings done ")


def find_similar_post(query, top_k=1):
    q_emb = get_embedding(query)
    scores = []

    for item in post_embeddings:
        score = cosine_similarity([q_emb], [item["embeddings"]])[0][0]
        scores.append((score, item["post"]))

    scores.sort(reverse=True, key=lambda x: x[0])

    return scores[:top_k]


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if client.user != message.author:
        if client.user in message.mentions:
            channel = message.channel

            query = message.content
            print("Query Message", query)
            best_match = find_similar_post(query=query)

            context = "\n \n".join([p["content"] for _, p in best_match])

            prompt = f"""
            Context :
            {context}

            Question:
            {query}


            Answer IN urdu 
            reply naturally using context 
            """

            # The client gets the API key from the environment variable `GEMINI_API_KEY`.
            clients = genai.Client(api_key=token_G)

            response = clients.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            print(response.text)

            await channel.send(response.text)


client.run(token)
