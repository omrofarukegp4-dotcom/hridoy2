import os
import requests
from ai_engine import ai_news
from design_engine import create_news_card


def post_news():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        res = requests.get(url, timeout=10)

        data = res.json()

        if "Data" not in data or len(data["Data"]) == 0:
            return

        news = data["Data"][0]

        title = news["title"]
        body = news["body"]

        # 🧠 AI TEXT
        ai_text = ai_news(title, body)

        # 🎨 IMAGE (news card)
        img = create_news_card(title)

        # 📡 Telegram send
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
        print("News error:", e)
