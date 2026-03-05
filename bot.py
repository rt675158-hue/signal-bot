import requests
import pandas as pd
import time

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

SYMBOLS = ["BTCUSDT","ETHUSDT","XRPUSDT","SOLUSDT"]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url,data=data)

def get_klines(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=100"
    data = requests.get(url).json()
    closes = [float(x[4]) for x in data]
    return pd.Series(closes)

def ema(series,period):
    return series.ewm(span=period).mean()

def rsi(series,period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100/(1+rs))
    return rsi

def generate_signal(price,e20,e50,r):
    if e20>e50 and r>55:
        return "BUY"
    if e20<e50 and r<45:
        return "SELL"
    return None

def risk_levels(price):
    entry=price
    sl=round(price*0.98,2)
    tp1=round(price*1.03,2)
    tp2=round(price*1.05,2)
    return entry,sl,tp1,tp2

while True:

    for symbol in SYMBOLS:

        series=get_klines(symbol)

        e20=ema(series,20).iloc[-1]
        e50=ema(series,50).iloc[-1]

        r=rsi(series).iloc[-1]

        price=series.iloc[-1]

        signal=generate_signal(price,e20,e50,r)

        if signal:

            entry,sl,tp1,tp2=risk_levels(price)

            message=f"""
CRYPTO SIGNAL

Coin: {symbol}

Signal: {signal}

Entry: {entry}

StopLoss: {sl}

TP1: {tp1}
TP2: {tp2}

RSI: {round(r,2)}
"""

            send_message(message)

    time.sleep(1500)
