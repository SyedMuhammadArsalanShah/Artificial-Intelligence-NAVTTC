# WhatsApp AI Bot with GPT-5 Nano

This project is a **WhatsApp AI bot** using **Meta's WhatsApp Cloud API** and **OpenAI GPT-5 Nano**. It receives WhatsApp messages and responds intelligently using AI. Built with **FastAPI** for async message handling.

---

## Features

* ✅ Receive WhatsApp messages via webhook
* ✅ Respond using GPT-5 Nano AI
* ✅ Only text messages supported; other media return a fallback message
* ✅ Fully async using FastAPI and httpx
* ✅ Easy setup with environment variables

---

## Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Setup WhatsApp Cloud API](#setup-whatsapp-cloud-api)
* [Environment Variables](#environment-variables)
* [Code Structure](#code-structure)
* [Running the App](#running-the-app)
* [Contributing](#contributing)
* [License](#license)

---

## Requirements

* Python 3.11+
* FastAPI
* httpx
* python-dotenv
* openai package
* ngrok (for local webhook testing)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/whatsapp-gpt-bot.git
cd whatsapp-gpt-bot

# Install dependencies
pip install fastapi uvicorn httpx python-dotenv openai

# Create a .env file
cp .env.example .env
```

---

## Setup WhatsApp Cloud API

Follow these steps to get your **System User**, **Access Token**, and **Phone Number ID**:

### 1️⃣ Create a Facebook App

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Click **My Apps → Create App → Business**
3. Enter app name and email → Click **Create App**

---

### 2️⃣ Set up WhatsApp API

1. Go to **Add Product → WhatsApp**
2. Click **Set Up WhatsApp Business API → Cloud API**

---

### 3️⃣ Create a System User

1. In **Meta Business Manager → Settings → Users → System Users**
2. Click **Add** → Name it → Assign **Admin role**
3. Generate token and assign **WhatsApp Business Account** with permissions:

   * `whatsapp_business_messaging`
   * `whatsapp_business_management`

Save the **Access Token**.

---

### 4️⃣ Get Phone Number ID

1. Go to **WhatsApp → Getting Started → Your Numbers**
2. Copy **Phone Number ID** for `.env`

---

### 5️⃣ Configure Webhook

1. Go to **WhatsApp → Webhooks → Add Webhook**
2. Use `https://your-domain.com/webhook` (or ngrok URL for local testing)
3. Set **Verify Token** (any random string, same as `.env`)

---

## Environment Variables

Create `.env` file:

```env
VERIFY_TOKEN=your_verify_token_here
WHATSAPP_TOKEN=your_whatsapp_cloud_api_token_here
PHONE_NUMBER_ID=your_phone_number_id_here
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Step-by-Step Code

We will divide the code into **logical steps** for clarity.

---

### Step 1: Import Dependencies & Load Environment Variables

```python
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import httpx
from openai import OpenAI

# Load environment variables
load_dotenv()
app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GRAPH_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# OpenAI GPT-5 Nano Client
client = OpenAI(api_key=OPENAI_API_KEY)
```

---

### Step 2: Webhook Verification Endpoint

This endpoint allows WhatsApp to verify your server.

```python
@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    print("VERIFY PARAMS =>", dict(params))

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge, status_code=200)

    raise HTTPException(status_code=403, detail="Verification failed")
```

---

### Step 3: Sending WhatsApp Messages

This function sends a text message back to the user.

```python
async def send_whatsapp_text(to: str, text: str):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    async with httpx.AsyncClient(timeout=20) as client_http:
        r = await client_http.post(GRAPH_URL, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()
```

---

### Step 4: AI Reply using GPT-5 Nano

This function generates AI responses from OpenAI GPT-5 Nano.

```python
async def get_ai_reply(user_text: str) -> str:
    if not OPENAI_API_KEY:
        return "AI is disabled. You said: " + user_text
    try:
        resp = client.responses.create(
            model="gpt-5-nano",
            input=user_text
        )
        return resp.output_text
    except Exception as e:
        return f"AI error: {e}"
```

---

### Step 5: Receiving WhatsApp Messages

This endpoint handles incoming WhatsApp messages via webhook.

```python
@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    try:
        entries = data.get("entry", [])
        for entry in entries:
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages")
                if not messages:
                    continue

                for msg in messages:
                    sender = msg["from"]
                    mtype = msg["type"]

                    if mtype == "text":
                        user_text = msg["text"]["body"]
                        ai_text = await get_ai_reply(user_text)
                        await send_whatsapp_text(sender, ai_text)
                    else:
                        await send_whatsapp_text(sender, "Please send text only.")
    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}
```

---

## Running the App

```bash
# Run FastAPI app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# If testing locally, use ngrok
ngrok http 8000
```

Use the **ngrok URL** as your webhook URL for testing.

---

## Folder Structure

```
whatsapp-gpt-bot/
├── main.py          # FastAPI app
├── .env             # Environment variables
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## Contributing

Fork → Branch → Pull Request.

---

## License

MIT License

---
