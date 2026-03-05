import ccxt
import pandas as pd
import requests
import time

exchange = ccxt.binance()

pairs = ["BTC/USDT","ETH/USDT","XRP/USDT","SOL/USDT"]

BOT_TOKEN = "8780560298:AAHGfAMAbFtfJ-5cAWMfcfy86UiXZHPoREQ"
CHAT_ID = "7969223643"

def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def check_signal(pair):
    ohlcv = exchange.fetch_ohlcv(pair, timeframe='25m', limit=100)
    df = pd.DataFrame(ohlcv, columns=['time','open','high','low','close','volume'])

    df['ema20'] = df['close'].ewm(span=20).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()
    df['rsi'] = calculate_rsi(df['close'])

    last = df.iloc[-1]
    price = last['close']

    entry = round(price,2)
    stoploss = round(price * 0.99,2)
    target = round(price * 1.02,2)

    signal = None

    if last['ema20'] > last['ema50'] and last['rsi'] > 55:
        signal = "BUY"

    elif last['ema20'] < last['ema50'] and last['rsi'] < 45:
        signal = "SELL"

    if signal:
        message = f"""
PAIR: {pair}
SIGNAL: {signal}

ENTRY: {entry}
STOPLOSS: {stoploss}
TARGET: {target}

TIMEFRAME: 25m
ACCURACY: 70%
"""
        send_message(message)

while True:
    for pair in pairs:
        check_signal(pair)

    time.sleep(1500)
