# 🤖 Discord Gemini Bot – Step-by-Step Setup Guide

This guide walks you through setting up a simple **Discord bot** that uses **Google Gemini (GenAI)** to respond when someone mentions the bot in a Discord server.

---

## 🧩 1. Prerequisites

Before starting, make sure you have:

* Python **3.10 or above** installed
* A **Discord bot token** (from [Discord Developer Portal](https://discord.com/developers/applications))
* A **Gemini (GenAI) API key** from [Google AI Studio](https://aistudio.google.com/)
* `pip` (Python package manager)

---

## 📁 2. Project Structure

```
discord-gemini-bot/
│
├── bot.py                # your bot code
├── requirements.txt      # dependencies
├── .env                  # your secret keys
└── README.md             # setup guide (this file)
```

---

## ⚙️ 3. Create and activate a virtual environment

```bash
# create project folder
mkdir discord-gemini-bot
cd discord-gemini-bot

# create virtual environment
python -m venv venv

# activate (Windows)
venv\Scripts\activate

# activate (Mac/Linux)
source venv/bin/activate
```

---

## 📦 4. Create `requirements.txt`

Create a file named **`requirements.txt`** and add:

```
python-dotenv
discord.py
google-genai
```

Now install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 5. Create `.env` file

Create a `.env` file in your project folder and add your API keys:

```
SECRET_KEY=YOUR_DISCORD_BOT_TOKEN_HERE
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

> ⚠️ **Never** share or upload this file publicly.
> Add `.env` to your `.gitignore` if you use Git.

---

## 🧠 6. Create your Discord bot (if not already done)

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** → Name it → Click **Create**
3. Go to **Bot** tab → Click **Add Bot** → Confirm
4. Copy your **Bot Token** (paste it into `SECRET_KEY` in `.env`)
5. Enable **MESSAGE CONTENT INTENT** under **Privileged Gateway Intents**
6. Go to **OAuth2 → URL Generator**

   * Scopes: `bot`
   * Permissions: `Send Messages`, `Read Messages/View Channels`
   * Copy the generated URL and invite your bot to your server

---

## 💻 7. Add your code to `bot.py`

Paste **your exact code** below into a file named `bot.py`:

```python
import os

from dotenv import load_dotenv
from google import genai

import discord

load_dotenv()
token = os.getenv("SECRET_KEY")
token_G = os.getenv("GEMINI_API_KEY")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if client.user != message.author:
        if client.user in message.mentions:
            channel = message.channel

            # The client gets the API key from the environment variable `GEMINI_API_KEY`.
            clients = genai.Client(api_key=token_G)

            response = clients.models.generate_content(
                model="gemini-2.5-flash", contents=message.content
            )
            print(response.text)

            await channel.send(response.text)

client.run(token)
```

---

## 🚀 8. Run the bot

Make sure you’re in your virtual environment and then run:

```bash
python bot.py
```

If everything works, you’ll see:

```
We have logged in as YourBotName
```

---

## 💬 9. Test the bot

1. Open your Discord server.
2. In any channel where the bot has access, mention it:

   ```
   @YourBotName Hello there!
   ```
3. The bot will send the message text to Gemini and reply with an AI-generated response.

---

## 🧾 10. Troubleshooting

| Problem                                         | Possible Fix                                                     |
| ----------------------------------------------- | ---------------------------------------------------------------- |
| **Bot not responding**                          | Ensure Message Content Intent is enabled in the Developer Portal |
| **`genai` module not found**                    | Run `pip install google-genai` again                             |
| **Invalid Token error**                         | Double-check your `SECRET_KEY` in `.env`                         |
| **Empty response or `response.text` not found** | Print `response` object to inspect its structure                 |
| **Bot not joining server**                      | Invite using correct OAuth2 URL with bot permissions             |

---

## 🧱 11. `.gitignore` (optional)

If you plan to use Git, create a `.gitignore` file:

```
venv/
__pycache__/
.env
*.pyc
```

---

## 🏁 12. Summary

✅ You created a Discord bot

✅ Connected it with Gemini (GenAI)

✅ Set up environment variables safely

✅ The bot replies when mentioned in a Discord channel

---

### 💡 Bonus Tips

* Keep `.env` private — never push it to GitHub.
* You can modify the `model` name (e.g., `"gemini-1.5-pro"`) for different AI behavior.
* For longer responses, you may split messages since Discord’s limit is 2000 characters.
* Want slash commands or persistent chat memory? That can be added later.

---

Developed by **Syed Muhammad Arsalan Shah Bukhari**
✨ *AI-powered Discord Integration using Gemini*
