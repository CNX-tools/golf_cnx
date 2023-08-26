import json
import os
import time
import requests

config_path = os.path.join(os.getcwd(), 'configuration', 'telegram.json')
with open(config_path, 'r', encoding='utf8') as f:
    config = json.load(f)
    TOKEN = config['token']
    CHAT_ID = config['chat_id']

BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'


def send_message(text):
    url = BASE_URL + 'sendMessage'
    payload = {
        'chat_id': '-927940414',
        'text': text
    }

    while True:
        try:
            response = requests.post(url, data=payload)
            break
        except:
            time.sleep(1)

    return response.json()
