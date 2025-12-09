import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import httpx
from openai import OpenAI

# ---------------- ENV & INIT ----------------
load_dotenv()
app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GRAPH_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# OpenAI GPT-5 Nano Client
client = OpenAI(api_key=OPENAI_API_KEY)


# ---------------- WEBHOOK VERIFICATION ----------------
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


# ---------------- SEND WHATSAPP TEXT ----------------
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


# ---------------- GPT-5 NANO AI REPLY ----------------
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


# ---------------- RECEIVE WHATSAPP MESSAGES ----------------
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
