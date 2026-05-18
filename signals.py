import os
import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
from ai_engine import ai_signal

SYMBOL = "BTCUSDT"


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


def generate_signal():
    df = get_data()

    if df is None or len(df) < 50:
        return None

    price = df["c"].iloc[-1]

    rsi = 45
    macd = "bullish"

    direction = "LONG" if rsi < 50 else "SHORT"

    caption = ai_signal(direction, price, rsi, macd)

    # simple chart
    plt.figure(figsize=(6,3))
    plt.plot(df["c"].tail(50))
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return caption, buf


def send_signal_photo(caption, image):
    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    requests.post(
        url,
        data={"chat_id": CHAT_ID, "caption": caption},
        files={"photo": image}
    )
