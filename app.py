import os
import time
import threading
import schedule
import requests
from flask import Flask

from signals import generate_signal, send_signal_photo
from news import post_news
from market import get_market_overview

# =========================
# ENV
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# FLASK APP
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Ultra AI Crypto Bot Running"

@app.route("/web")
def web():
    return "OK"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# =========================
# TELEGRAM TEXT
# =========================
def send_text(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "HTML"
        })
    except Exception as e:
        print("Telegram error:", e)

# =========================
# JOBS
# =========================
def signal_job():
    try:
        result = generate_signal()
        if result:
            caption, img = result
            send_signal_photo(caption, img)
    except Exception as e:
        print("Signal error:", e)

def news_job():
    try:
        post_news()
    except Exception as e:
        print("News error:", e)

def market_job():
    try:
        msg = get_market_overview()
        send_text(msg)
    except Exception as e:
        print("Market error:", e)

def run_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)

# =========================
# SCHEDULE
# =========================
schedule.every(15).minutes.do(signal_job)
schedule.every(30).minutes.do(news_job)
schedule.every(4).hours.do(market_job)

# =========================
# MAIN (IMPORTANT FIX)
# =========================
if __name__ == "__main__":
    print("🔥 Bot Starting...")

    # initial run
    signal_job()
    news_job()
    market_job()

    # scheduler thread
    t1 = threading.Thread(target=run_bot, daemon=True)
    t1.start()

    # FLASK MUST RUN MAIN THREAD
    run_server()
