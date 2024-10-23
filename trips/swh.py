import requests
from config import TOKEN_TBOT

whook = '35999c6678c3bf.lhr.life'

r = requests.get(f'https://api.telegram.org/bot{TOKEN_TBOT}/setWebhook?url=https://{whook}/')

print(r.json())