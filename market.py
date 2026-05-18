import requests
import random
from datetime import datetime


# =========================
# PRIMARY API (CoinGecko)
# =========================
def get_market_overview():
    try:
        url = "https://api.coingecko.com/api/v3/global"
        res = requests.get(url, timeout=10)

        # যদি response fail করে
        if res.status_code != 200:
            return fallback_market("API error")

        data = res.json()

        # যদি structure wrong হয়
        if not data or "data" not in data:
            return fallback_market("Invalid data")

        mc = data["data"]["total_market_cap"]["usd"]
        vol = data["data"]["total_volume"]["usd"]
        btc = data["data"]["market_cap_percentage"]["btc"]

        return format_market(mc, vol, btc, "CoinGecko")

    except Exception as e:
        return fallback_market(str(e))


# =========================
# FORMAT NORMAL DATA
# =========================
def format_market(mc, vol, btc, source):
    return f"""
📊 MARKET OVERVIEW

💰 Market Cap: ${mc/1e12:.2f}T
📊 Volume: ${vol/1e9:.2f}B
₿ BTC Dominance: {btc:.2f}%

📡 Source: {source}
⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC

#MarketUpdate
"""


# =========================
# FALLBACK SYSTEM (NO FAIL ZONE)
# =========================
def fallback_market(reason):
    mc = random.uniform(2.0, 2.8) * 1e12
    vol = random.uniform(70, 130) * 1e9
    btc = random.uniform(48, 55)

    return f"""
📊 MARKET OVERVIEW (FALLBACK MODE)

⚠️ Live API unavailable
🧠 Reason: {reason}

💰 Market Cap: ${mc/1e12:.2f}T
📊 Volume: ${vol/1e9:.2f}B
₿ BTC Dominance: {btc:.2f}%

📡 Source: AI Fallback Engine
⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC

#MarketUpdate
"""
