import os
import requests

posted = []

def post_news():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return

        data = res.json()

        if not data or "Data" not in data:
            return

        if len(data["Data"]) == 0:
            return

        news = data["Data"][0]

        if news["url"] in posted:
            return

        posted.append(news["url"])

        msg = f"""
📰 CRYPTO NEWS

{news['title']}

{news['body'][:200]}...

#CryptoNews
"""

        TOKEN = os.getenv("BOT_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg}
        )

    except Exception as e:
        print("News error:", e)
