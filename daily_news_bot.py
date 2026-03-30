import requests
import datetime
import os

# LINE Notify 設定 (RenderのEnvironment Variablesから読み込む)
# ローカル実行時は .env ファイルから読み込む設定
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")

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
        print(f"Error sending LINE Notify: {e}")
        return None

def get_news():
    # 実際にはここにスクレイピングなどのロジックが入りますが、現在はサンプルを返します
    today = datetime.date.today().strftime("%Y/%m/%d")
    news_content = f"\n【{today} ニュースまとめ】\n\n"
    
    news_content += "■ AIニュース\n・Metaが次世代AIチップを発表。2027年配備予定。\n\n"
    news_content += "■ 日経ニュース\n・円相場が1ドル=160円台へ下落。1年8カ月ぶり水準。\n\n"
    news_content += "■ BBCニュース\n・トランプ大統領、5月に訪中し習近平国家主席と会談へ。"
    return news_content

def main():
    # Render環境に合わせてログの出力先を相対パスに変更
    log_path = "daily_news_bot.log"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[{now}] Starting news collection...")
    news_message = get_news()
    
    print(f"[{now}] Sending to LINE...")
    status = send_line_notify(news_message)
    
    # ログ記録
    with open(log_path, "a", encoding="utf-8") as f:
        if status == 200:
            log_msg = f"[{now}] Success: News sent to LINE.\n"
        else:
            log_msg = f"[{now}] Error: Failed (Status: {status}).\n"
        f.write(log_msg)
        print(log_msg.strip())

if __name__ == "__main__":
    main()