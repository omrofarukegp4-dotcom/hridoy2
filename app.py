import os
import time
import threading
import schedule
import requests
from flask import Flask

# =========================
# MODULE IMPORTS
# =========================
from signals import generate_signal, send_signal_photo
from news import post_news
from market import get_market_overview

# =========================
# ENV VARIABLES
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# FLASK APP (KEEP ALIVE)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Ultra AI Crypto Empire Running"

@app.route("/web")
def web():
    return "OK - Bot Alive"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# =========================
# TELEGRAM TEXT SENDER
# =========================
def send_text(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        })
    except Exception as e:
        print("Telegram error:", e)

# =========================
# SIGNAL JOB
# =========================
def signal_job():
    try:
        result = generate_signal()
        if result:
            caption, image = result
            send_signal_photo(caption, image)
            print("✅ Signal sent")
    except Exception as e:
        print("Signal error:", e)

# =========================
# NEWS JOB (ULTRA AI READY)
# =========================
def news_job():
    try:
        post_news()
        print("📰 News sent")
    except Exception as e:
        print("News error:", e)

# =========================
# MARKET JOB
# =========================
def market_job():
    try:
        msg = get_market_overview()
        send_text(msg)
        print("📊 Market sent")
    except Exception as e:
        print("Market error:", e)

# =========================
# SCHEDULE SETUP
# =========================
schedule.every(15).minutes.do(signal_job)
schedule.every(30).minutes.do(news_job)
schedule.every(4).hours.do(market_job)

# =========================
# BOT LOOP
# =========================
def run_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)

# =========================
# START EVERYTHING
# =========================
if __name__ == "__main__":
    print("🔥 Ultra AI Crypto Empire Starting...")

    # First run instantly
    signal_job()
    news_job()
    market_job()

    # Threads
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_server)

    t1.daemon = True
    t2.daemon = True

    t1.start()
    t2.start()
