import requests

BOT_TOKEN = "8780560298:AAHGfAMAbFtfJ-5cAWMfcfy86UiXZHPoREQ"
CHAT_ID = "7969223643"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

data = {
 "chat_id": CHAT_ID,
 "text": "Bot working test"
}

requests.post(url,data=data)
