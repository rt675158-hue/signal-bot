import requests
import pandas as pd

BOT_TOKEN = "8780560298:AAHGfAMAbFtfJ-5cAWMfcfy86UiXZHPoREQ"
CHAT_ID = "7969223643"

SYMBOL = "BTCUSDT"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url,data=data)

def get_klines():

    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval=15m&limit=100"

    data = requests.get(url).json()

    closes = []

    for x in data:
        if isinstance(x,list) and len(x) > 4:
            closes.append(float(x[4]))

    return pd.Series(closes)

def ema(series,n):
    return series.ewm(span=n).mean()

def rsi(series,period=14):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100/(1+rs))


s = get_klines()

ema20 = ema(s,20).iloc[-1]
ema50 = ema(s,50).iloc[-1]

rsi_val = rsi(s).iloc[-1]

price = s.iloc[-1]

if ema20 > ema50 and rsi_val > 55:

    entry = price
    sl = round(price*0.98,2)
    tp = round(price*1.04,2)

    msg=f"""
BUY SIGNAL

Coin: {SYMBOL}

Entry: {entry}
StopLoss: {sl}
TakeProfit: {tp}
"""

    send(msg)

elif ema20 < ema50 and rsi_val < 45:

    entry = price
    sl = round(price*1.02,2)
    tp = round(price*0.96,2)

    msg=f"""
SELL SIGNAL

Coin: {SYMBOL}

Entry: {entry}
StopLoss: {sl}
TakeProfit: {tp}
"""

    send(msg)

else:

    send("No trading signal now")
