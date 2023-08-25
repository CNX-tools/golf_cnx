import requests

TOKEN = '6555382573:AAEuidPng_9KA80Hj1gBosBSqz3Nat9U2oI'
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'


def send_message(text):
    url = BASE_URL + 'sendMessage'
    payload = {
        'chat_id': '-927940414',
        'text': text
    }
    response = requests.post(url, data=payload)
    return response.json()
