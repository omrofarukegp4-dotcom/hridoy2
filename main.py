import os
import requests
import schedule
import time
import feedparser
from bs4 import BeautifulSoup
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/web')
def home():
    return "Bot is running perfectly on /web!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

NEWS_FEEDS = [
    'https://coingape.com/feed/',
    'https://cointelegraph.com/rss',
    'https://www.coindesk.com/arc/outboundfeeds/rss/'
]
AIRDROP_FEED = 'https://airdrops.io/feed/'
EXCHANGE_FEED = 'https://cryptonews.com/news/exchange-news/feed/'

posted_news_links = []
posted_airdrop_links = []
posted_exchange_links = []

def get_feed_data(rss_url):
    try:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            return None
            
        latest_entry = feed.entries[0]
        title = latest_entry.title
        link = latest_entry.link
        
        soup = BeautifulSoup(latest_entry.description, "html.parser")
        summary = soup.get_text()[:250] + "..." 
        
        image_url = None
        if 'media_content' in latest_entry:
            image_url = latest_entry.media_content[0]['url']
        elif 'enclosures' in latest_entry and len(latest_entry.enclosures) > 0:
            image_url = latest_entry.enclosures[0]['href']
        else:
            img_tag = soup.find('img')
            if img_tag and img_tag.has_attr('src'):
                image_url = img_tag['src']
                
        return {"title": title, "link": link, "summary": summary, "image": image_url}
    except Exception as e:
        print(f"Error ({rss_url}):", e)
        return None

def send_to_telegram(data, caption):
    try:
        if data['image']:
            api_url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
            payload = {"chat_id": CHAT_ID, "photo": data['image'], "caption": caption, "parse_mode": "Markdown"}
        else:
            api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            payload = {"chat_id": CHAT_ID, "text": caption, "parse_mode": "Markdown"}
            
        response = requests.post(api_url, data=payload)
        return response.status_code == 200
    except Exception as e:
        print("Telegram error:", e)
        return False

def post_news():
    global posted_news_links
    for url in NEWS_FEEDS:
        news = get_feed_data(url)
        if news and news['link'] not in posted_news_links:
            caption = (
                f"🚨 **{news['title']}**\n\n"
                f"🗞 {news['summary']}"
            )
            if send_to_telegram(news, caption):
                print(f"Success: {news['title']}")
                posted_news_links.append(news['link'])
                if len(posted_news_links) > 50:
                    posted_news_links.pop(0)
            time.sleep(3)

def post_airdrop():
    global posted_airdrop_links
    airdrop = get_feed_data(AIRDROP_FEED)
    if airdrop and airdrop['link'] not in posted_airdrop_links:
        caption = (
            f"🎁 **New Official Airdrop: {airdrop['title']}**\n\n"
            f"📝 **Details:**\n{airdrop['summary']}\n\n"
            f"⚠️ *Don't miss out on this opportunity!*"
        )
        if send_to_telegram(airdrop, caption):
            print(f"Success: {airdrop['title']}")
            posted_airdrop_links.append(airdrop['link'])
            if len(posted_airdrop_links) > 20:
                posted_airdrop_links.pop(0)

def post_exchange_event():
    global posted_exchange_links
    event = get_feed_data(EXCHANGE_FEED)
    if event and event['link'] not in posted_exchange_links:
        caption = (
            f"🏦 **Exchange Update & Event: {event['title']}**\n\n"
            f"📅 **Details:**\n{event['summary']}\n\n"
            f"📢 *Stay updated with market events!*"
        )
        if send_to_telegram(event, caption):
            print(f"Success: {event['title']}")
            posted_exchange_links.append(event['link'])
            if len(posted_exchange_links) > 20:
                posted_exchange_links.pop(0)

schedule.every(10).minutes.do(post_news)
schedule.every(1).hours.do(post_airdrop)
schedule.every(2).hours.do(post_exchange_event)

if __name__ == "__main__":
    print("Bot starting...")
    
    post_news()
    post_airdrop()
    post_exchange_event()
    
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
