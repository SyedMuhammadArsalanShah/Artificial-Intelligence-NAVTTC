# smasb_bot_api.py
"""
SMASB BOT - FastAPI RAG Backend
Author: Syed Muhammad Arsalan Shah Bukhari
Organization: SMASB (Syed Muhammad Arsalan Shah Bukhari)
Description:
    AI-powered Retrieval-Augmented Generation (RAG) system.
    Retrieves relevant content from curated knowledge (Facebook posts)
    and generates simple Urdu answers using Gemini LLM.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bs4 import BeautifulSoup
import os, json, numpy as np, joblib
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from tiktoken import encoding_for_model
from openai import OpenAI
from google import genai

# =====================================================
# Load Environment Variables
# =====================================================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not OPENAI_API_KEY or not GEMINI_API_KEY:
    raise RuntimeError("Missing API keys in environment variables")

# =====================================================
# FastAPI App Initialization
# =====================================================
app = FastAPI(
    title="SMASB BOT",
    version="1.0.0",
    description="""
    SMASB BOT is an AI-powered Retrieval-Augmented Generation (RAG) system
    developed and maintained by SMASB
    (Syed Muhammad Arsalan Shah Bukhari).
    It retrieves knowledge from curated content and provides answers in simple Urdu.
    """,
    contact={
        "name": "Syed Muhammad Arsalan Shah Bukhari",
        "organization": "SMASB"
    }
)

# =====================================================
# Data Loading & Scraping
# =====================================================
HTML_FILE = "fbpost.html"
JSON_FILE = "facebook_posts.json"
EMBED_FILE = "embeddings.joblib"

if not os.path.exists(JSON_FILE):
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    posts = [
        {"post": i, "content": p.get_text(strip=True)}
        for i, p in enumerate(soup.find_all("div", class_="_2pin"), start=1)
    ]
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
else:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

# =====================================================
# Embedding Functions
# =====================================================
enc = encoding_for_model("text-embedding-3-small")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def chunk_text(text, max_tokens=7000):
    tokens = enc.encode(text)
    return [enc.decode(tokens[i:i + max_tokens]) for i in range(0, len(tokens), max_tokens)]

def get_embeddings(text):
    vectors = []
    for chunk in chunk_text(text):
        emb = openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        ).data[0].embedding
        vectors.append(np.array(emb))
    return vectors

if os.path.exists(EMBED_FILE):
    post_embeddings = joblib.load(EMBED_FILE)
else:
    post_embeddings = [
        {"post": p, "embeddings": get_embeddings(p["content"])}
        for p in posts
    ]
    joblib.dump(post_embeddings, EMBED_FILE)

# =====================================================
# Similarity Search
# =====================================================
def find_best_post(query):
    query_embeddings = get_embeddings(query)
    best_score = 0
    best_post = None

    for item in post_embeddings:
        for q in query_embeddings:
            for p in item["embeddings"]:
                score = cosine_similarity([q], [p])[0][0]
                if score > best_score:
                    best_score = score
                    best_post = item["post"]

    return best_post

# =====================================================
# API Request/Response Models
# =====================================================
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    source_post: int

# =====================================================
# API Endpoints
# =====================================================
@app.get("/")
def health_check():
    return {"status": "ok", "message": "SMASB BOT API running"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(payload: QueryRequest):
    post = find_best_post(payload.question)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="کوئی متعلقہ پوسٹ نہیں ملی"
        )

    prompt = f"""
Context:
{post['content']}

Question:
{payload.question}

Answer in simple Urdu.
"""

    gemini = genai.Client(api_key=GEMINI_API_KEY)
    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text,
        "source_post": post["post"]
    }
