import requests
import time
import pandas as pd

BOT_TOKEN = "8780560298:AAHGfAMAbFtfJ-5cAWMfcfy86UiXZHPoREQ"
CHAT_ID = "7969223643"

symbols = [
"BTCUSDT",
"ETHUSDT",
"XRPUSDT",
"SOLUSDT"
]

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url,data=data)


def get_klines(symbol):

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=100"

    data = requests.get(url).json()

    close_prices = [float(candle[4]) for candle in data]

    return pd.Series(close_prices)


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


def generate_signal(price,ema20,ema50,rsi):

    if ema20 > ema50 and rsi > 55:
        return "BUY"

    if ema20 < ema50 and rsi < 45:
        return "SELL"

    return None


def risk_levels(price):

    entry = price

    sl = round(price * 0.98,2)

    tp1 = round(price * 1.03,2)

    tp2 = round(price * 1.05,2)

    return entry,sl,tp1,tp2


while True:

    for symbol in symbols:

        prices = get_klines(symbol)

        ema20 = ema(prices,20).iloc[-1]

        ema50 = ema(prices,50).iloc[-1]

        rsi_val = rsi(prices).iloc[-1]

        price = prices.iloc[-1]

        signal = generate_signal(price,ema20,ema50,rsi_val)

        if signal:

            entry,sl,tp1,tp2 = risk_levels(price)

            message = f"""
📊 CRYPTO SIGNAL

Coin: {symbol}

Signal: {signal}

Entry: {entry}

Stop Loss: {sl}

TP1: {tp1}
TP2: {tp2}

RSI: {round(rsi_val,2)}
"""

            send_message(message)

    time.sleep(1500)
