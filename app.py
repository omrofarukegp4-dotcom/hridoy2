import os
import time
import threading
import schedule
from flask import Flask

from news import post_news
from market import post_market
from airdrop import post_airdrop
from exchange import post_exchange

# optional SMM (if enabled)
try:
    from smm_panel import boost_post
    SMM_ENABLED = True
except:
    SMM_ENABLED = False


# =========================
# 🌐 FLASK APP (RENDER KEEP ALIVE)
# =========================
app = Flask(__name__)


@app.route("/")
def home():
    return "🚀 Crypto Media Bot is LIVE"


@app.route("/health")
def health():
    return "OK"


# =========================
# 🔥 WRAPPERS (POST + BOOST)
# =========================

def handle_post(post_func):
    """
    Generic handler:
    1. Post content
    2. Get Telegram post URL (must return from function)
    3. Optional SMM boost
    """

    try:
        post_url = post_func()

        if post_url and SMM_ENABLED:
            boost_post(post_url)

    except Exception as e:
        print("Handler error:", e)


def news_job():
    handle_post(post_news)


def market_job():
    handle_post(post_market)


def airdrop_job():
    handle_post(post_airdrop)


def exchange_job():
    handle_post(post_exchange)


# =========================
# ⏰ SCHEDULER
# =========================
def start_scheduler():
    print("🚀 Scheduler started...")

    schedule.every(30).minutes.do(news_job)
    schedule.every(3).hours.do(market_job)
    schedule.every(2).hours.do(airdrop_job)
    schedule.every(1).hours.do(exchange_job)

    while True:
        schedule.run_pending()
        time.sleep(1)


# =========================
# 🚀 START SERVER
# =========================
if __name__ == "__main__":
    print("🔥 Starting Crypto Media System...")

    # background thread
    t = threading.Thread(target=start_scheduler)
    t.daemon = True
    t.start()

    # Render port
    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
