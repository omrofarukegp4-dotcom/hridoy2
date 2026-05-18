import os
import requests
from ai_engine import ai_news

posted = []


def post_news():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        res = requests.get(url, timeout=10)

        data = res.json()

        if "Data" not in data or len(data["Data"]) == 0:
            return

        news = data["Data"][0]

        if news["url"] in posted:
            return

        posted.append(news["url"])

        ai_post = ai_news(news["title"], news["body"])

        TOKEN = os.getenv("BOT_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": ai_post,
                "parse_mode": "HTML"
            }
        )

    except Exception as e:
        print("News error:", e)
