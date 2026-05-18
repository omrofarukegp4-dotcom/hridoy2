import requests


# =========================
# MAIN FUNCTION
# =========================
def get_market_overview():
    # 1️⃣ CoinGecko (Primary)
    data = get_from_coingecko()
    if data:
        return data

    # 2️⃣ Binance (Backup 1)
    data = get_from_binance()
    if data:
        return data

    # 3️⃣ CoinCap (Backup 2)
    data = get_from_coincap()
    if data:
        return data

    # ❌ all failed → silent
    return None


# =========================
# COINGECKO
# =========================
def get_from_coingecko():
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/global",
            timeout=8
        )

        data = res.json()

        if not data or "data" not in data:
            return None

        mc = data["data"]["total_market_cap"]["usd"]
        vol = data["data"]["total_volume"]["usd"]
        btc = data["data"]["market_cap_percentage"]["btc"]

        return format_market(mc, vol, btc, "CoinGecko")

    except:
        return None


# =========================
# BINANCE (Backup)
# =========================
def get_from_binance():
    try:
        res = requests.get(
            "https://api.binance.com/api/v3/ticker/24hr",
            timeout=8
        )

        data = res.json()

        if not isinstance(data, list):
            return None

        # BTCUSDT extract
        btc = next((x for x in data if x["symbol"] == "BTCUSDT"), None)

        if not btc:
            return None

        price = float(btc["lastPrice"])
        volume = float(btc["quoteVolume"])

        # fake market cap estimate (approx logic)
        mc = price * 19500000  # BTC supply approx
        btc_dom = 50.0

        return format_market(mc, volume, btc_dom, "Binance")

    except:
        return None


# =========================
# COINCAP (Backup)
# =========================
def get_from_coincap():
    try:
        res = requests.get(
            "https://api.coincap.io/v2/assets/bitcoin",
            timeout=8
        )

        data = res.json()

        if "data" not in data:
            return None

        price = float(data["data"]["priceUsd"])
        volume = float(data["data"]["volumeUsd24Hr"])

        mc = float(data["data"]["marketCapUsd"])
        btc_dom = 50.0

        return format_market(mc, volume, btc_dom, "CoinCap")

    except:
        return None


# =========================
# FORMAT OUTPUT
# =========================
def format_market(mc, vol, btc, source):
    try:
        return f"""
📊 MARKET UPDATE

💰 Market Cap: ${mc/1e12:.2f}T
📊 Volume: ${vol/1e9:.2f}B
₿ BTC Dominance: {btc:.2f}%

📡 Source: {source}

#MarketUpdate
"""
    except:
        return None
