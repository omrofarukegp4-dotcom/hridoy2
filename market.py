import requests
from ai_engine import ai_market


def get_market_overview():
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/global",
            timeout=10
        )

        data = res.json()

        if "data" not in data:
            return "Market unavailable"

        mc = data["data"]["total_market_cap"]["usd"]
        vol = data["data"]["total_volume"]["usd"]
        btc = data["data"]["market_cap_percentage"]["btc"]

        raw = f"""
Market Cap: {mc}
Volume: {vol}
BTC Dominance: {btc}
"""

        return ai_market(raw)

    except:
        return "Market error"
