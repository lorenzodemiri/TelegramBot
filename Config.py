TOKEN = '931954383:AAEAKHnT1EXySuCu-NT7CSFp7LZs0w-AeGM'
NGROK_URL = 'https://e8bd2010.ngrok.io'
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
LOCAL_WEBHOOK_ENDPOINT = '{}/webhook'.format(NGROK_URL)
TELEGRAM_INIT_WEBHOOK_URL = '{}/setWebhook?url={}'.format(BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
TELEGRAM_DELETE_WEBHOOK_URL = '{}/setWebhook?url='.format(BASE_TELEGRAM_URL)
TELEGRAM_SEND_MESSAGE_URL = 'https://api.telegram.org/bot{}/deleteWebhook'.format(TOKEN)
TELEGRAM_CHANNELL_ID = '-1001273248107'
LINK_TABLE_ORDERS = 'https://docs.google.com/spreadsheets/d/1ar1NvJlUar5-m5aYmvS-IwJxOrTzmiDGUUMdRi98MJY/edit?usp=sharing'
TOKEN_ADMINBOT = '1049266407:AAGlAiS64UdAXH2uGdiZkrWWoyrEdjYwAfc'
TELEGRAM_CHANNELL_ID_PUBLIC = '-1001369590564'
URL_STORE_BOT = 'http://t.me/MubbyLabBot'
ADMIN_PASSWORD = '123Valbona'
INSTAGRAM_USERNAME = "mubbylab"
INSTAGRAM_PASSWORD = "aceroregon67"