import yfinance as yf
import ta

def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def add_rsi(data, window_length=14):
    data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=window_length).rsi()
    return data

def add_macd(data):
    macd = ta.trend.MACD(data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()
    data['MACD_Hist'] = macd.macd_diff()
    return data
