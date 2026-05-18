import matplotlib.pyplot as plt
import io


# =========================
# 📰 NEWS DESIGN CARD
# =========================
def create_news_card(title, sentiment="NEUTRAL"):
    plt.figure(figsize=(6, 3))
    plt.title("CRYPTO NEWS", fontsize=16)

    color = "green" if sentiment == "BULLISH" else "red" if sentiment == "BEARISH" else "blue"

    plt.text(
        0.5, 0.5,
        title,
        ha="center",
        wrap=True,
        fontsize=12,
        color=color
    )

    plt.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


# =========================
# 📈 SIGNAL CHART CARD
# =========================
def create_signal_chart(df, entry, tp, sl):
    plt.figure(figsize=(6, 3))

    plt.plot(df["c"].tail(50), linewidth=2)

    plt.axhline(entry, linestyle="--")
    plt.axhline(tp, linestyle="--", color="green")
    plt.axhline(sl, linestyle="--", color="red")

    plt.title("AI TRADING SIGNAL")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf


# =========================
# 📊 MARKET DASHBOARD
# =========================
def create_market_dashboard(mc, vol, btc):
    plt.figure(figsize=(6, 3))

    labels = ["Market Cap", "Volume", "BTC Dom"]
    values = [mc / 1e12, vol / 1e9, btc]

    plt.bar(labels, values)

    plt.title("CRYPTO MARKET OVERVIEW")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf
