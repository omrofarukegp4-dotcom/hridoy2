import os
import requests

OPENAI_KEY = os.getenv("OPENAI_KEY")


def call_ai(prompt):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]


# =========================
# 📰 NEWS AI WRITER
# =========================
def ai_news(title, body):
    prompt = f"""
You are a crypto news journalist.

Rewrite this into a professional Telegram crypto news post.

Rules:
- catchy headline
- short paragraphs
- simple English
- add emojis
- add hashtags
- mention market impact

News:
Title: {title}
Body: {body}
"""
    return call_ai(prompt)


# =========================
# 📊 MARKET AI WRITER
# =========================
def ai_market(text):
    prompt = f"""
You are a crypto market analyst.

Turn this data into a professional market report.

Rules:
- clear headline
- bullish/bearish tone
- simple explanation
- emojis
- hashtags

Data:
{text}
"""
    return call_ai(prompt)


# =========================
# 📈 SIGNAL AI EXPLAINER
# =========================
def ai_signal(direction, price, rsi, macd):
    prompt = f"""
You are a professional crypto trader.

Explain this trading signal like a hedge fund analyst.

Data:
Direction: {direction}
Price: {price}
RSI: {rsi}
MACD: {macd}

Include:
- why signal happened
- market logic
- risk note
- simple summary
- emojis
"""
    return call_ai(prompt)
