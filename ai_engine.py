
import os
import requests
import json

OPENAI_KEY = os.getenv("OPENAI_KEY")


# =========================
# GPT CALL ENGINE
# =========================
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

    res = requests.post(url, headers=headers, json=data).json()

    return res["choices"][0]["message"]["content"]


# =========================
# 📰 ULTRA NEWS BRAIN
# =========================
def ultra_ai_news(title, body):

    prompt = f"""
You are a senior crypto market analyst working for a hedge fund.

Analyze this news and provide:

1. Catchy headline
2. Rewritten professional crypto news
3. Sentiment (Bullish / Bearish / Neutral)
4. Impact score (1-10)
5. Expected short-term market reaction
6. Institutional involvement signal (Yes/No + reason)
7. 5 hashtags

News:
Title: {title}
Body: {body}

Return JSON:
{{
"headline": "",
"text": "",
"sentiment": "",
"impact": "",
"short_term_reaction": "",
"institutional_signal": "",
"hashtags": ""
}}
"""

    return json.loads(call_ai(prompt))


# =========================
# 🧠 ULTRA SIGNAL BRAIN
# =========================
def ultra_ai_signal(direction, rsi, macd_status, price, atr):

    prompt = f"""
You are a professional quant crypto trader.

Analyze this trading signal and explain it like a hedge fund desk.

Data:
Direction: {direction}
RSI: {rsi}
MACD Status: {macd_status}
Price: {price}
ATR (volatility): {atr}

Provide:

1. Why this signal happened
2. Market structure reasoning
3. Trend strength analysis
4. Risk warning (important)
5. Confidence score (0-100)
6. Simple summary for retail traders

Return JSON:
{{
"reason": "",
"market_structure": "",
"trend_strength": "",
"risk_warning": "",
"confidence": "",
"summary": ""
}}
"""

    return json.loads(call_ai(prompt))


# =========================
# 🔥 MARKET PSYCHOLOGY BRAIN
# =========================
def market_psychology(price_change, volume_spike):

    prompt = f"""
You are a crypto market psychologist.

Analyze market emotions:

Price Change %: {price_change}
Volume Spike: {volume_spike}

Provide:
- Fear or Greed state
- Market emotion explanation
- احتمال next move (up/down/sideways)
- Warning if manipulation possible

Return JSON:
{{
"emotion": "",
"explanation": "",
"next_move": "",
"warning": ""
}}
"""

    return json.loads(call_ai(prompt))
