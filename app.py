import time
import threading
import schedule

from news import post_news
from market import get_market_overview
from signals import generate_signal, send_signal_photo


# =========================
# 🔥 STARTUP LOG
# =========================
print("🚀 AI Crypto Media Bot Starting...")


# =========================
# 📰 NEWS JOB
# =========================
def news_job():
    try:
        post_news()
    except Exception as e:
        print("News job error:", e)


# =========================
# 📊 MARKET JOB
# =========================
def market_job():
    try:
        get_market_overview()
    except Exception as e:
        print("Market job error:", e)


# =========================
# 📈 SIGNAL JOB
# =========================
def signal_job():
    try:
        result = generate_signal()

        if result is None:
            return

        caption, image = result

        send_signal_photo(caption, image)

    except Exception as e:
        print("Signal job error:", e)


# =========================
# ⏰ SCHEDULER SETUP
# =========================
schedule.every(30).minutes.do(news_job)     # 📰 News
schedule.every(3).hours.do(market_job)      # 📊 Market
schedule.every(15).minutes.do(signal_job)   # 📈 Signals


# =========================
# 🔁 BACKGROUND LOOP
# =========================
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# =========================
# 🚀 MAIN START
# =========================
if __name__ == "__main__":
    thread = threading.Thread(target=run_scheduler)
    thread.daemon = True
    thread.start()

    print("✅ Bot is running...")

    # keep alive (Render/UptimeRobot friendly)
    while True:
        time.sleep(60)
