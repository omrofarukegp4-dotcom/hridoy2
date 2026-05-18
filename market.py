import requests

def get_market_overview():
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/global",
            timeout=10
        )

        data = res.json()

        # safety check
        if not isinstance(data, dict) or "data" not in data:
            return "📊 Market data temporarily unavailable"

        mc = data["data"]["total_market_cap"]["usd"]
        vol = data["data"]["total_volume"]["usd"]
        btc = data["data"]["market_cap_percentage"]["btc"]

        return f"""
📊 MARKET OVERVIEW

💰 Market Cap: ${mc/1e12:.2f}T
📊 Volume: ${vol/1e9:.2f}B
₿ BTC Dominance: {btc:.2f}%

#MarketUpdate
"""

    except Exception as e:
        return "📊 Market service unavailable"
