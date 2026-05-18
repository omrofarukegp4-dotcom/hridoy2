import os
import requests
import pandas as pd
import io
from ai_engine import ai_signal
from design_engine import create_signal_chart


SYMBOL = "BTCUSDT"


# =========================
# GET DATA
# =========================
def get_data():
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval=15m&limit=100"
        data = requests.get(url, timeout=10).json()

        if not isinstance(data, list):
            return None

        df = pd.DataFrame(data)
        df = df.iloc[:, 0:6]
        df.columns = ["t","o","h","l","c","v"]
        df["c"] = df["c"].astype(float)

        return df
    except:
        return None


# =========================
# SIGNAL GENERATOR
# =========================
def generate_signal():
    df = get_data()

    if df is None or len(df) < 50:
        return None

    price = df["c"].iloc[-1]

    direction = "LONG" if price % 2 == 0 else "SHORT"  # simple logic

    rsi = 45
    macd = "bullish"

    entry = price
    tp = price * 1.03
    sl = price * 0.98

    # 🧠 AI TEXT
    ai_text = ai_signal(direction, price, rsi, macd)

    # 🎨 IMAGE
    img = create_signal_chart(df, entry, tp, sl)

    return ai_text, img


# =========================
# SEND TO TELEGRAM
# =========================
def send_signal_photo(caption, image):
    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "caption": caption,
            "parse_mode": "HTML"
        },
        files={"photo": image}
    )
