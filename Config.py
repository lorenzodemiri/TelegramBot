TOKEN = 'INSERT PASSWORD HERE'
NGROK_URL = 'https://e8bd2010.ngrok.io'
BASE_TELEGRAM_URL = 'https://api.telegram.org/bot{}'.format(TOKEN)
LOCAL_WEBHOOK_ENDPOINT = '{}/webhook'.format(NGROK_URL)
TELEGRAM_INIT_WEBHOOK_UL = '{}/setWebhook?url={}'.format(BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
TELEGRAM_DELETE_WEBHOOK_URL = '{}/setWebhook?url='.format(BASE_TELEGRAM_URL)
TELEGRAM_SEND_MESSAGE_URL = 'https://api.telegram.org/bot{}/deleteWebhook'.format(TOKEN)
TELEGRAM_CHANNELL_ID = 'Channel Id' #Telegram Channel Id
LINK_TABLE_ORDERS = 'https://docs.google.com/spreadsheets/d/1ar1NvJlUar5-m5aYmvS-IwJxOrTzmiDGUUMdRi98MJY/edit?usp=sharing'
TOKEN_ADMINBOT = 'TOKEN ADMIN BOT' #token admin bot
TELEGRAM_CHANNELL_ID_PUBLIC = '-1001369590564'
URL_STORE_BOT = 'http://t.me/MubbyLabBot'
ADMIN_PASSWORD = 'Password'
INSTAGRAM_USERNAME = "mubbylab"
INSTAGRAM_PASSWORD = "instagram password" #instagram password