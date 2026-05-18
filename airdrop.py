import os
import requests
from ai_engine import call_ai
from design_engine import airdrop_card


def post_airdrop():
    try:
        res = requests.get("https://airdrops.io/feed/", timeout=10)

        if res.status_code != 200:
            return

        text = res.text[:2000]

        prompt = f"""
Extract crypto airdrop info.
Make it short Telegram post.
Warn if risky.

{text}
"""

        ai_text = call_ai(prompt)
        if not ai_text:
            return

        img = airdrop_card("New Crypto Airdrop Available")

        send(ai_text, img)

    except Exception as e:
        print("Airdrop error:", e)


def send(text, image):
    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    requests.post(
        url,
        data={"chat_id": CHAT_ID, "caption": text},
        files={"photo": image}
    )
