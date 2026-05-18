import os
import requests
from ai_engine import ai_market
from design_engine import create_market_dashboard


def get_market_overview():
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/global",
            timeout=10
        )

        data = res.json()

        if "data" not in data:
            return

        mc = data["data"]["total_market_cap"]["usd"]
        vol = data["data"]["total_volume"]["usd"]
        btc = data["data"]["market_cap_percentage"]["btc"]

        # 🧠 AI TEXT
        raw_text = f"""
Market Cap: {mc}
Volume: {vol}
BTC Dominance: {btc}
"""

        ai_text = ai_market(raw_text)

        # 🎨 IMAGE
        img = create_market_dashboard(mc, vol, btc)

        # 📡 Telegram
        TOKEN = os.getenv("BOT_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")

        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": ai_text,
                "parse_mode": "HTML"
            },
            files={"photo": img}
        )

    except Exception as e:
        print("Market error:", e)
