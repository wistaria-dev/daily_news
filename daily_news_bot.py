import requests
import datetime
import os
import feedparser

# LINE Notify 設定
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")

# ニュース取得元（RSSフィード）のリスト
RSS_URLS = {
    "AI・IT": "https://www.itmedia.co.jp/news/subtop/ai/index.xml",
    "日経・ビジネス": "https://www.nikkei.com/rss/news/business.xml",
    "海外（ロイター）": "https://jp.reuters.com/rssfeed/topNews",
    "海外（BBC）": "https://www.bbc.com/japanese/index.xml"
}

def send_line_notify(message):
    if not LINE_NOTIFY_TOKEN:
        print("Error: LINE_NOTIFY_TOKEN is not set.")
        return None
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}'}
    data = {'message': message}
    try:
        response = requests.post(line_notify_api, headers=headers, data=data)
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_news_from_rss(label, url, limit=3):
    """RSSから記事タイトルとリンクを取得する"""
    feed = feedparser.parse(url)
    text = f"■ {label}\n"
    
    # 記事が取れなかった場合の処理
    if not feed.entries:
        return text + "・ニュースを取得できませんでした。\n\n"

    for i, entry in enumerate(feed.entries[:limit]):
        text += f"・{entry.title}\n  {entry.link}\n"
    
    return text + "\n"

def main():
    today = datetime.date.today().strftime("%Y/%m/%d")
    news_message = f"\n【{today} ニュースまとめ】\n\n"

    # 各ジャンルのニュースを取得
    for label, url in RSS_URLS.items():
        # BBCとロイターは合わせて「海外」として取得
        limit = 2 if "海外" in label else 3
        news_message += get_news_from_rss(label, url, limit=limit)

    # 最後に定型文を挿入
    news_message += "本日も一日頑張りましょう！"

    print("Sending to LINE...")
    status = send_line_notify(news_message)
    
    if status == 200:
        print("Success!")
    else:
        print(f"Failed: {status}")

if __name__ == "__main__":
    main()