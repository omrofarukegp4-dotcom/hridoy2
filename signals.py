import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime

SYMBOL = "BTCUSDT"
LIMIT = 200

posted = []

# =========================
# GET DATA SAFE
# =========================
def get_data():
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval=15m&limit={LIMIT}"
        res = requests.get(url, timeout=10)
        data = res.json()

        if not isinstance(data, list) or len(data) == 0:
            return None

        df = pd.DataFrame(data)
        df = df.iloc[:, 0:6]
        df.columns = ["t","o","h","l","c","v"]

        df["c"] = df["c"].astype(float)
        return df

    except:
        return None


# =========================
# INDICATORS
# =========================
def indicators(df):
    try:
        delta = df["c"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        rs = gain.rolling(14).mean() / loss.rolling(14).mean()
        df["RSI"] = 100 - (100 / (1 + rs))

        ema12 = df["c"].ewm(span=12).mean()
        ema26 = df["c"].ewm(span=26).mean()

        df["MACD"] = ema12 - ema26
        df["SIGNAL"] = df["MACD"].ewm(span=9).mean()

        return df

    except:
        return None


# =========================
# CHART
# =========================
def create_chart(df):
    plt.figure(figsize=(8,4))
    plt.plot(df["c"].tail(50))
    plt.title("AI Signal Chart")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


# =========================
# SIGNAL ENGINE
# =========================
def generate_signal():
    global posted

    df = get_data()

    if df is None or df.empty or len(df) < 50:
        return None

    df = indicators(df)

    if df is None or df.empty:
        return None

    last = df.tail(1).iloc[0]

    price = last["c"]

    direction = None

    if last["RSI"] < 35 and last["MACD"] > last["SIGNAL"]:
        direction = "LONG"
        sl = price * 0.98
        tp = price * 1.04

    elif last["RSI"] > 65 and last["MACD"] < last["SIGNAL"]:
        direction = "SHORT"
        sl = price * 1.02
        tp = price * 0.96

    else:
        return None

    signal_id = f"{direction}-{round(price)}"

    if signal_id in posted:
        return None

    posted.append(signal_id)
    if len(posted) > 30:
        posted.pop(0)

    img = create_chart(df)

    caption = f"""
🚀 AI SIGNAL

📊 Pair: {SYMBOL}
📈 Direction: {direction}
💰 Entry: {price:.2f}
🛑 SL: {sl:.2f}
🎯 TP: {tp:.2f}

⏰ {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC
"""

    return caption, img


# =========================
# TELEGRAM PHOTO
# =========================
def send_signal_photo(caption, image):
    try:
        TOKEN = os.getenv("BOT_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")

        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

        requests.post(url, data={
            "chat_id": CHAT_ID,
            "caption": caption,
            "parse_mode": "HTML"
        }, files={"photo": image})

    except Exception as e:
        print("Telegram error:", e)
