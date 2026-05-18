import os
import requests

posted = []

def post_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    res = requests.get(url).json()

    if "Data" not in res:
        return

    news = res["Data"][0]

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
