import requests
import pandas as pd
import time

BOT_TOKEN = "8780560298:AAHGfAMAbFtfJ-5cAWMfcfy86UiXZHPoREQ"
CHAT_ID = "7969223643"

SYMBOL = "BTCUSDT"

def send(msg):
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data={"chat_id":CHAT_ID,"text":msg}
    requests.post(url,data=data)

def get_klines():
    url=f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval=15m&limit=100"
    data=requests.get(url).json()

    closes=[]

    for x in data:
        if isinstance(x,list) and len(x)>4:
            closes.append(float(x[4]))

    return pd.Series(closes)

def ema(series,n):
    return series.ewm(span=n).mean()

while True:

    series=get_klines()

    if len(series)==0:
        time.sleep(60)
        continue

    e20=ema(series,20).iloc[-1]
    e50=ema(series,50).iloc[-1]

    price=series.iloc[-1]

    if e20>e50:
        signal="BUY"
    else:
        signal="SELL"

    entry=price
    sl=round(price*0.98,2)
    tp=round(price*1.04,2)

    msg=f"""
ALGO SIGNAL

Coin: {SYMBOL}

Signal: {signal}

Entry: {entry}

StopLoss: {sl}

TakeProfit: {tp}
"""

    send(msg)

    time.sleep(1500)
