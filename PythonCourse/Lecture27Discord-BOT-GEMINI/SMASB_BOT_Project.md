

# **📚 Lecture: Building an AI-Powered Discord Bot with Facebook Post Retrieval**

**Instructor:** Syed Muhammad Arsalan Shah Bukhari

**Level:** Beginner → Intermediate (Python + AI)

**Duration:** ~2 hours

**Goal:** Teach students to build a professional Discord bot using **web scraping, embeddings, similarity search, AI response generation, and deployment**.

---

## **1️⃣ Learning Objectives**

By the end of this lecture, students will be able to:

1. Extract Facebook posts from HTML using **BeautifulSoup**
2. Convert text posts into **vector embeddings** using OpenAI
3. Use **cosine similarity** to find the most relevant post
4. Build a **Discord bot** that interacts with users
5. Generate **AI-based contextual answers** using Google Gemini API
6. Understand **chunking** for handling long texts efficiently
7. Structure Python projects professionally (modular files & mega file)
8. Deploy the bot **locally or on cloud platforms**

---

## **2️⃣ Project Overview**

**Workflow:**

1. HTML (Facebook posts) → Scraper → JSON file
2. JSON → Embeddings → `.joblib` file
3. Discord query → Similarity search → Best post
4. Post + Query → Gemini AI → Answer
5. Bot replies on Discord

**Visual Diagram (Premium)**

![Premium Flow Diagram](https://github-production-user-asset-6210df.s3.amazonaws.com/77351219/528867584-11144b34-dd63-4c77-a6fd-5659e50b6c18.png?X-Amz-Algorithm=AWS4-HMAC-SHA256\&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20251220%2Fus-east-1%2Fs3%2Faws4_request\&X-Amz-Date=20251220T112216Z\&X-Amz-Expires=300\&X-Amz-Signature=3bd80726a21bd9137f339f493ce0cd7b1249941370cb83b61764e86880fc2b31\&X-Amz-SignedHeaders=host)

> Colors, icons, and arrows indicate the **step-by-step flow** from data extraction to user reply.

---

## **3️⃣ File Structure (Professional)**

```
AI_DiscordBot_Project/
│
├─ .env                    # API keys (Discord, OpenAI, Gemini)
├─ requirements.txt        # Required Python libraries
├─ fbpost.html              # Raw Facebook posts HTML
├─ fb_scraper.py            # Scraper → facebook_posts.json
├─ embeddings_manager.py    # Convert text → embeddings
├─ similarity_search.py     # Find most similar post
├─ discord_bot.py           # Main Discord bot logic
├─ mega_ai_discord_bot.py   # One-file complete project (demo version)
├─ facebook_posts.json      # Auto-generated JSON
└─ embeddings.joblib        # Auto-generated embeddings
```

> Students can also use a **mega single file** for quick demo purposes before modularizing.

---

## **4️⃣ Step 1: Web Scraping Facebook Posts**

```python
from bs4 import BeautifulSoup
import json

file_path = "fbpost.html"

with open(file_path, "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")
posts = soup.find_all("div", class_="_2pin")

data = []
for idx, post in enumerate(posts, start=1):
    data.append({"post": idx, "content": post.get_text(strip=True)})

with open("facebook_posts.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Extracted {len(data)} posts")
```

> **Explanation:** Parses HTML → extracts posts → stores as JSON.
> Reference: [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/)

---

## **5️⃣ Step 2: Generate Embeddings**

```python
import json, os, numpy as np, joblib
from openai import OpenAI
from tiktoken import encoding_for_model

with open("facebook_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

enc = encoding_for_model("text-embedding-3-small")
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
```

> **Explanation:** Converts text into vectors; uses chunking to handle long posts.
> Reference: OpenAI Embeddings Docs

---

## **6️⃣ Step 3: Find Similar Posts (Cosine Similarity)**

```python
from sklearn.metrics.pairwise import cosine_similarity
from embeddings_manager import post_embeddings, get_embedding_safe

def find_similar_post(query):
    query_embeddings = get_embedding_safe(query)
    best_score, best_post = 0, None

    for post_item in post_embeddings:
        for query_chunk in query_embeddings:
            for post_chunk in post_item["embeddings"]:
                score = cosine_similarity([query_chunk], [post_chunk])[0][0]
                if score > best_score:
                    best_score = score
                    best_post = post_item["post"]
    return best_post
```

> **Explanation:** Compares query embeddings to posts → returns most relevant.
> Reference: [Scikit-Learn Cosine Similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)

---

## **7️⃣ Step 4: Discord Bot**

```python
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
    if message.author == client.user: return
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
        response = gemini.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        await message.channel.send(response.text)

client.run(DISCORD_TOKEN)
```

> **Explanation:** Detects mentions → finds similar post → sends context to Gemini → replies.
> Reference: [Discord.py Docs](https://discordpy.readthedocs.io)

---

## **8️⃣ Optional: Mega Single File (Complete Demo)**

```python
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
with open("fbpost.html","r",encoding="utf-8") as f: html=f.read()
soup=BeautifulSoup(html,"html.parser")
posts=[{"post":i,"content":p.get_text(strip=True)} for i,p in enumerate(soup.find_all("div",class_="_2pin"),start=1)]
with open("facebook_posts.json","w",encoding="utf-8") as f: json.dump(posts,f,ensure_ascii=False,indent=2)

# Embeddings
enc=encoding_for_model("text-embedding-3-small")
openai_client=OpenAI(api_key=OPENAI_API_KEY)
def chunk_text(text,max_tokens=7000): tokens=enc.encode(text); return [enc.decode(tokens[i:i+max_tokens]) for i in range(0,len(tokens),max_tokens)]
def get_embeddings(text): return [np.array(openai_client.embeddings.create(input=chunk,model="text-embedding-3-small").data[0].embedding) for chunk in chunk_text(text)]
if os.path.exists("embeddings.joblib"): post_embeddings=joblib.load("embeddings.joblib")
else: post_embeddings=[{"post":p,"embeddings":get_embeddings(p["content"])} for p in posts]; joblib.dump(post_embeddings,"embeddings.joblib")

# Similarity
def find_best_post(query):
    query_embeddings=get_embeddings(query)
    best_score,best_post=0,None
    for item in post_embeddings:
        for q in query_embeddings:
            for p in item["embeddings"]:
                score=cosine_similarity([q],[p])[0][0]
                if score>best_score: best_score,best_post=score,item["post"]
    return best_post

# Discord Bot
intents=discord.Intents.default(); intents.message_content=True
client=discord.Client(intents=intents)

@client.event
async def on_ready(): print(f"Bot logged in as {client.user}")
@client.event
async def on_message(message):
    if message.author==client.user: return
    if client.user in message.mentions:
        query=message.content
        post=find_best_post(query)
        if not post: await message.channel.send("معذرت، کوئی متعلقہ پوسٹ نہیں ملی."); return
        prompt=f"Context:\n{post['content']}\n\nQuestion:\n{query}\n\nAnswer in simple Urdu."
        gemini=genai.Client(api_key=GEMINI_API_KEY)
        response=gemini.models.generate_content(model="gemini-2.5-flash",contents=prompt)
        await message.channel.send(response.text)

client.run(DISCORD_TOKEN)
```

---

## **9️⃣ requirements.txt**

```txt
beautifulsoup4
discord.py
python-dotenv
scikit-learn
numpy
joblib
tiktoken
openai
google-generativeai
```

> Install with: `pip install -r requirements.txt`

---

## **1️⃣0️⃣ Key References & Tools**

| Concept           | Source                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| BeautifulSoup     | [https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/) |
| OpenAI Embeddings | [https://platform.openai.com/docs](https://platform.openai.com/docs)                             |
| Cosine similarity | Scikit-Learn docs                                                                                |
| Discord.py        | [https://discordpy.readthedocs.io](https://discordpy.readthedocs.io)                             |
| Google Gemini API | [https://ai.google.dev](https://ai.google.dev)                                                   |

---

## **1️⃣1️⃣ Tips for Students**

1. Understand each step separately: Scraping → Embeddings → Similarity → Discord Bot
2. Use **chunking** for long posts to avoid embedding errors
3. Test each module individually before integrating
4. Use **mega file** for quick demo; modular files for professional projects
5. Visual diagram helps follow the **full workflow** from raw data → AI → user reply

---

## **1️⃣2️⃣ Deployment: Running Your AI Discord Bot**

Once the bot is ready locally, students can **deploy it** so it runs **24/7**. There are multiple options:

---

### **A) Local Deployment (for Testing)**

1. Open terminal/command prompt in project folder.
2. Ensure `.env` has correct API keys.
3. Activate virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

4. Install requirements:

```bash
pip install -r requirements.txt
```

5. Run the bot:

```bash
python discord_bot.py
```

> The bot should log in and respond to mentions in your server.

---

### **B) Cloud Deployment (for 24/7 Bot)**

**Popular options:**

#### 1️⃣ **Replit**

* Free tier for testing small bots.
* Create a new Python project → Upload all files + `.env`.
* Set environment variables in Replit Secrets.
* Click **Run** → bot goes live.
* Optionally use **UptimeRobot** to keep the bot alive.

#### 2️⃣ **Render**

* Sign up at [render.com](https://render.com/).
* Create **Web Service** → GitHub repo of your project.
* Add environment variables for Discord, OpenAI, Gemini API.
* Automatic deployments when you push code updates.

#### 3️⃣ **Heroku (Legacy, but still usable)**

* Sign up at [heroku.com](https://www.heroku.com/)
* Install Heroku CLI
* Push project → Set config vars → Scale dyno to run bot continuously.

---

### **C) Tips for Deployment**

1. **Keep `.env` secure** – never commit API keys to GitHub public repos.
2. **Use Mega File for Demo**: simpler to deploy a single Python script.
3. **Logging**: Add `print()` or logging for debugging.
4. **Monitor Bot**: Use uptime monitoring tools to avoid downtime.

---

### **D) Optional: Docker Deployment**

* Dockerize your bot for **containerized, portable deployment**:

```dockerfile
# Dockerfile example
FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "discord_bot.py"]
```

* Build & run container:

```bash
docker build -t ai-discord-bot .
docker run -d ai-discord-bot
```

> Professional-grade deployment for **portfolio-ready projects**.

---

### ✅ **Deployment Summary**

* Test locally first.
* Use cloud services (Replit, Render, Heroku) for 24/7 availability.
* Secure API keys & logs.
* Optional Docker container for portability and professional delivery.

---

## **📌 Conclusion (Gist)**

*This project teaches how to build a professional AI Discord bot by:*

* Scraping Facebook posts into JSON
* Converting text into vector embeddings
* Searching for the most relevant post using cosine similarity
* Integrating with Discord for real-time interaction
* Using Google Gemini AI to generate contextual answers

> **Key Takeaway:** Students now understand **end-to-end AI pipeline**, modular coding, deployment, and real-world bot integration in Python.

---
