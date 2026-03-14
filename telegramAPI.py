from typing import Final
from urllib.parse import quote, urlencode,quote_plus
import requests
from dotenv import load_dotenv
import os

load_dotenv()


TOKEN: Final = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME: Final = "@togetitdone_bot"
CHAT_ID:Final="-1003621093424"

def sendBot(message):
   
    message = quote_plus(message)
    
    send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + message
    try:
       response = requests.get(send_text)
       if not response.json()['ok']:
            print(response.json())
       return response.json()
       
    except Exception as e:
        print(e)
