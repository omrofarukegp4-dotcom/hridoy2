import os
import time
import threading
import schedule
from flask import Flask

from news import post_news
from market import post_market
from airdrop import post_airdrop
from exchange import post_exchange


# =========================
# 🌐 FLASK APP (RENDER KEEP ALIVE)
# =========================
app = Flask(__name__)


@app.route("/")
def home():
    return "🚀 Crypto Media Bot is Running"


@app.route("/health")
def health():
    return "OK"


# =========================
# 🔥 BACKGROUND TASKS
# =========================
def start_scheduler():
    print("🚀 Scheduler started...")

    schedule.every(30).minutes.do(post_news)
    schedule.every(3).hours.do(post_market)
    schedule.every(2).hours.do(post_airdrop)
    schedule.every(1).hours.do(post_exchange)

    while True:
        schedule.run_pending()
        time.sleep(1)


# =========================
# 🚀 START APP
# =========================
if __name__ == "__main__":
    print("🔥 Starting AI Crypto Media Bot...")

    # background thread
    t = threading.Thread(target=start_scheduler)
    t.daemon = True
    t.start()

    # Render port fix
    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
