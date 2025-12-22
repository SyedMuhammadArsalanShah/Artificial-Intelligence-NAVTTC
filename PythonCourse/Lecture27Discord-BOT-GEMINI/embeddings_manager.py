import json, os, numpy as np, joblib
from openai import OpenAI
from tiktoken import encoding_for_model
from dotenv import load_dotenv

with open("facebook_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

enc = encoding_for_model("text-embedding-3-small")
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def chunk_text(text, max_tokens=7000):
    tokens = enc.encode(text)
    return [enc.decode(tokens[i:i+max_tokens]) for i in range(0, len(tokens), max_tokens)]

def get_embedding_safe(text):
    if not text.strip(): return []
    client = OpenAI(api_key=OPENAI_API_KEY)
    embeddings = []
    for chunk in chunk_text(text):
        response = client.embeddings.create(input=chunk, model="text-embedding-3-small")
        embeddings.append(np.array(response.data[0].embedding))
    return embeddings

if os.path.exists("embeddings.joblib"):
    post_embeddings = joblib.load("embeddings.joblib")
else:
    post_embeddings = [{"post": p, "embeddings": get_embedding_safe(p["content"])} for p in posts if p["content"].strip()]
    joblib.dump(post_embeddings, "embeddings.joblib")