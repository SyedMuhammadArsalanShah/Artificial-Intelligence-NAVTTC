# fastapi_app.py
import os
import json
import time
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

import numpy as np
import joblib

# Replace these with the SDKs you use (OpenAI / genai)
from openai import OpenAI
from google import genai

from sklearn.metrics.pairwise import cosine_similarity
from tiktoken import encoding_for_model

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(title="Embeddings + Search + Answer API")

# ---------- Config ----------
EMBEDDINGS_FILE = Path("embeddings.joblib")
POSTS_FILE = Path("facebook_posts.json")  # your dataset
EMBED_MODEL = "text-embedding-3-small"
ENC_MODEL = "text-embedding-3-small"
MAX_TOKENS_PER_CHUNK = 7000

# ---------- Helpers ----------
enc = encoding_for_model(ENC_MODEL)


def chunk_text(text: str, max_tokens: int = MAX_TOKENS_PER_CHUNK) -> List[str]:
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunks.append(enc.decode(chunk_tokens))
    return chunks


def get_embeddings_with_openai(text: str) -> List[np.ndarray]:
    """Return list of numpy vectors (one per chunk)."""
    if not text or not text.strip():
        return []
    client = OpenAI(api_key=OPENAI_API_KEY)
    chunks = chunk_text(text)
    vectors = []
    for chunk in chunks:
        resp = client.embeddings.create(input=chunk, model=EMBED_MODEL)
        vec = np.array(resp.data[0].embedding, dtype=np.float32)
        vectors.append(vec)
    return vectors


def get_embeddings_with_gemini(text: str) -> List[np.ndarray]:
    """Alternative: use Gemini embeddings via genai if you prefer."""
    if not text or not text.strip():
        return []
    clients = genai.Client(api_key=GEMINI_API_KEY)
    # Note: Adjust to real gemini embedding call if available
    # Below is a placeholder pattern for demonstration; replace with actual call if different.
    chunks = chunk_text(text)
    vectors = []
    for chunk in chunks:
        response = clients.embeddings.create(model="embedtext-1", input=chunk)
        vec = np.array(response.data[0].embedding, dtype=np.float32)
        vectors.append(vec)
    return vectors


# ---------- Load / build embeddings ----------
def load_posts() -> List[dict]:
    if not POSTS_FILE.exists():
        raise RuntimeError(f"{POSTS_FILE} not found. Add your dataset JSON.")
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_and_save_embeddings(use_provider: str = "openai"):
    posts = load_posts()
    out = []
    for p in posts:
        content = p.get("content", "") or ""
        if not content.strip():
            continue
        if use_provider == "openai":
            vectors = get_embeddings_with_openai(content)
        else:
            vectors = get_embeddings_with_gemini(content)
        out.append({"post": p, "embeddings": vectors})
    joblib.dump(out, EMBEDDINGS_FILE)
    return out


def load_embeddings():
    if EMBEDDINGS_FILE.exists():
        return joblib.load(EMBEDDINGS_FILE)
    else:
        return build_and_save_embeddings()


post_embeddings = load_embeddings()


# ---------- Pydantic models ----------
class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3
    provider: Optional[str] = "openai"  # "openai" or "gemini"


class AnswerRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3
    model: Optional[str] = "gemini-2.5-flash"  # choose your LLM


# ---------- Endpoints ----------
@app.get("/health")
def health():
    return {"status": "ok", "time": time.time()}


@app.post("/search")
def search(req: SearchRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Empty query")

    if req.provider == "openai":
        q_vectors = get_embeddings_with_openai(req.query)
    else:
        q_vectors = get_embeddings_with_gemini(req.query)

    if not q_vectors:
        return {"results": []}

    scores = []
    for item in post_embeddings:
        # compute similarity between any pair of query chunk and post chunk and take max
        max_score = 0.0
        for qv in q_vectors:
            for pv in item["embeddings"]:
                score = float(cosine_similarity([qv], [pv])[0][0])
                if score > max_score:
                    max_score = score
        scores.append({"score": max_score, "post": item["post"]})

    scores.sort(key=lambda x: x["score"], reverse=True)
    top_results = scores[: req.top_k]
    return {"results": top_results}


@app.post("/answer")
def answer(req: AnswerRequest):
    # Search first
    from fastapi import BackgroundTasks

    search_req = SearchRequest(query=req.query, top_k=req.top_k)
    search_res = search(search_req)
    contexts = [r["post"]["content"] for r in search_res["results"]]

    prompt = "---\n".join(contexts) + f"\n\nQuestion: {req.query}\nAnswer in Urdu using the context above."

    # Call Gemini or OpenAI for completion
    # Here we use genai (Gemini) by default because original code used it
    clients = genai.Client(api_key=GEMINI_API_KEY)
    response = clients.models.generate_content(model=req.model, contents=prompt)

    return {"answer": response.text, "contexts": contexts, "raw": response}


# Endpoint to rebuild embeddings (admin)
@app.post("/rebuild-embeddings")
def rebuild(provider: Optional[str] = "openai"):
    global post_embeddings
    post_embeddings = build_and_save_embeddings(use_provider=provider)
    return {"status": "built", "count": len(post_embeddings)}
