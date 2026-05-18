import matplotlib.pyplot as plt
import io


# =========================
# 📰 NEWS IMAGE
# =========================
def news_card(title):
    plt.figure(figsize=(6,3))
    plt.title("CRYPTO NEWS", fontsize=14)
    plt.text(0.5, 0.5, title, ha="center", wrap=True)
    plt.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


# =========================
# 📊 MARKET IMAGE
# =========================
def market_card(mc, vol, btc):
    plt.figure(figsize=(6,3))

    labels = ["Market Cap", "Volume", "BTC Dom"]
    values = [mc/1e12, vol/1e9, btc]

    plt.bar(labels, values)
    plt.title("MARKET OVERVIEW")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


# =========================
# 🎁 AIRDROP IMAGE
# =========================
def airdrop_card(title):
    plt.figure(figsize=(6,3))
    plt.title("AIRDROP ALERT", fontsize=14)
    plt.text(0.5, 0.5, title, ha="center", wrap=True)
    plt.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


# =========================
# 🏦 EXCHANGE IMAGE
# =========================
def exchange_card(title):
    plt.figure(figsize=(6,3))
    plt.title("EXCHANGE UPDATE", fontsize=14)
    plt.text(0.5, 0.5, title, ha="center", wrap=True)
    plt.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf
