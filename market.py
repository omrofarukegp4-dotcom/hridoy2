import os
import requests
from ai_engine import ai_market
from design_engine import market_card


def post_market():
    try:
        res = requests.get("https://api.coingecko.com/api/v3/global")
        data = res.json()["data"]

        mc = data["total_market_cap"]["usd"]
        vol = data["total_volume"]["usd"]
        btc = data["market_cap_percentage"]["btc"]

        raw = f"MC:{mc} VOL:{vol} BTC:{btc}"
        ai_text = ai_market(raw)

        img = market_card(mc, vol, btc)

        send(ai_text, img)

    except Exception as e:
        print("Market error:", e)


def send(text, image):
    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    requests.post(
        url,
        data={"chat_id": CHAT_ID, "caption": text},
        files={"photo": image}
    )
