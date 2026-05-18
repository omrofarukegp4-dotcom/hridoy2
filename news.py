import os
import requests
from ai_engine import ai_news
from design_engine import news_card


def post_news():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        res = requests.get(url, timeout=10)
        data = res.json()

        news = data["Data"][0]

        title = news["title"]
        body = news["body"]

        ai_text = ai_news(title, body)
        img = news_card(title)

        send(ai_text, img)

    except Exception as e:
        print("News error:", e)


def send(text, image):
    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    requests.post(
        url,
        data={"chat_id": CHAT_ID, "caption": text},
        files={"photo": image}
    )
