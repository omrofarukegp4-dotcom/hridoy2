import requests

def get_market_overview():
    data = requests.get("https://api.coingecko.com/api/v3/global").json()

    mc = data["data"]["total_market_cap"]["usd"]
    vol = data["data"]["total_volume"]["usd"]
    btc = data["data"]["market_cap_percentage"]["btc"]

    return f"""
📊 MARKET OVERVIEW

Market Cap: ${mc/1e12:.2f}T
Volume: ${vol/1e9:.2f}B
BTC Dominance: {btc:.2f}%

#MarketUpdate
"""
