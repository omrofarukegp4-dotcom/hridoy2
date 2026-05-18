import os
import requests

OPENAI_KEY = os.getenv("OPENAI_KEY")


# =========================
# BASE AI CALL FUNCTION
# =========================
def call_ai(prompt):
    try:
        if not OPENAI_KEY:
            return None

        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }

        res = requests.post(url, headers=headers, json=payload, timeout=15)

        data = res.json()

        return data["choices"][0]["message"]["content"]

    except:
        return None


# =========================
# 📰 NEWS AI WRITER
# =========================
def ai_news(title, body):
    prompt = f"""
You are a professional crypto news journalist.

Rewrite this into a Telegram crypto news post.

Rules:
- catchy headline
- short paragraphs
- simple English
- add emojis
- add hashtags
- include market impact (bullish/bearish/neutral)

News:
Title: {title}
Body: {body}
"""

    result = call_ai(prompt)

    if result:
        return result

    # fallback
    return f"""
📰 CRYPTO NEWS

{title}

{body[:200]}...

#CryptoNews
"""


# =========================
# 📊 MARKET ANALYST AI
# =========================
def ai_market(raw_text):
    prompt = f"""
You are a crypto market analyst.

Turn this into a professional market report.

Rules:
- clear headline
- bullish/bearish/neutral tone
- simple explanation
- emojis
- hashtags
- short and readable

Data:
{raw_text}
"""

    result = call_ai(prompt)

    if result:
        return result

    # fallback
    return f"""
📊 MARKET UPDATE

{raw_text}

#MarketUpdate
"""


# =========================
# 📈 SIGNAL AI EXPLAINER
# =========================
def ai_signal(direction, price, rsi, macd):
    prompt = f"""
You are a professional crypto trader (institutional level).

Explain this trading signal.

Rules:
- why signal triggered
- market logic
- risk explanation
- simple summary
- emojis
- no overcomplication

Data:
Direction: {direction}
Price: {price}
RSI: {rsi}
MACD: {macd}
"""

    result = call_ai(prompt)

    if result:
        return result

    # fallback
    return f"""
🚀 {direction} SIGNAL

Price: {price}
RSI: {rsi}
MACD: {macd}

Simple AI analysis unavailable (fallback mode)
"""


# =========================
# 🧠 SENTIMENT ANALYZER (OPTIONAL BOOST)
# =========================
def ai_sentiment(text):
    prompt = f"""
Analyze crypto market sentiment.

Return only one word:
BULLISH / BEARISH / NEUTRAL

Text:
{text}
"""

    result = call_ai(prompt)

    if result:
        return result.strip().upper()

    return "NEUTRAL"
