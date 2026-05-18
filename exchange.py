import os
import requests
from ai_engine import call_ai
from design_engine import exchange_card


def post_exchange():
    try:
        res = requests.get("https://www.binance.com/en/support/announcement", timeout=10)

        if res.status_code != 200:
            return

        text = res.text[:2000]

        prompt = f"""
Extract exchange events:
- listings
- updates
- trading events

Make Telegram post.

{text}
"""

        ai_text = call_ai(prompt)
        if not ai_text:
            return

        img = exchange_card("Exchange Update")

        send(ai_text, img)

    except Exception as e:
        print("Exchange error:", e)


def send(text, image):
    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    requests.post(
        url,
        data={"chat_id": CHAT_ID, "caption": text},
        files={"photo": image}
    )
