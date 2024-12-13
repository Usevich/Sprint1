import yfinance as yf
import ta

def fetch_stock_data(ticker, period='1mo', start_date=None, end_date=None):
    stock = yf.Ticker(ticker)
    if start_date and end_date:
        data = stock.history(start=start_date, end=end_date)
    else:
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
