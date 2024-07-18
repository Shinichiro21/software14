import requests
from bs4 import BeautifulSoup
import json
import re

# Yahoo天気の東京の天気ページURL
url = 'https://weather.yahoo.co.jp/weather/jp/13/4410.html'

# ページの内容を取得
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 天気情報を取得
weather_info = soup.find('p', class_='pict').text.strip()

# 降水確率を取得
precipitation_info = soup.find('tr', class_='precip')
if precipitation_info:
    val_info = precipitation_info.find('td', class_='val')
    if val_info:
        precipitation_text = val_info.text.strip()
        # 正規表現を使用して数値のみを抽出する
        precipitation_percentage = re.search(r'\d+', precipitation_text)
        if precipitation_percentage:
            precipitation_probability = int(precipitation_percentage.group())
        else:
            precipitation_probability = 0  # デフォルト値
    else:
        precipitation_probability = 0  # デフォルト値
else:
    precipitation_probability = 0  # デフォルト値

# メッセージを作成
message = f'天気: {weather_info}\n降水確率: {precipitation_probability}%\n'

# 日傘か雨傘が必要か判断
if '雨' in weather_info:
    message += '雨が予想されています。雨傘を持っていきましょう。'
elif '晴' in weather_info:
    if precipitation_probability <= 30:
        message += '快晴ですが、日傘が必要です。'
    else:
        message += '快晴です。日傘が必要です。'
else:
    message += '日傘及び雨傘の両方を準備しましょう。'

# Slack Webhook URL
slack_webhook_url = 'https://hooks.slack.com/services/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'

# Slackに通知を送信
payload = {'text': message}
requests.post(slack_webhook_url, data=json.dumps(payload))

print('通知を送信しました。')
