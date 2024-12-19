import yfinance as yf
import ta


def fetch_stock_data(ticker, period='1mo', start_date=None, end_date=None):
    """
        Загружает исторические данные по акции с использованием библиотеки yfinance.

        Параметры:
            ticker (str): Тикер акции (например, "AAPL" для Apple).
            period (str, optional): Период данных в формате yfinance (например, '1mo', '1y').
                                    По умолчанию '1mo'.
            start_date (str, optional): Дата начала периода (в формате 'YYYY-MM-DD'). Если указаны
                                        start_date и end_date, они имеют приоритет над period.
            end_date (str, optional): Дата конца периода (в формате 'YYYY-MM-DD').

        Возвращает:
            pandas.DataFrame: Данные по цене и объемам акций, включая открытие (Open),
                              закрытие (Close), самый высокий (High), самый низкий (Low) уровни цен
                              и объем (Volume).
    """
    stock = yf.Ticker(ticker)
    if start_date and end_date:
        data = stock.history(start=start_date, end=end_date)
    else:
        data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    """
        Добавляет в DataFrame скользящую среднюю (Moving Average) по заданному периоду.

        Параметры:
            data (pandas.DataFrame): Данные акций с историческими ценами. Должен содержать столбец 'Close'.
            window_size (int, optional): Размер окна для расчёта скользящей средней. По умолчанию 5.

        Возвращает:
            pandas.DataFrame: Исходный DataFrame с добавленным столбцом 'Moving_Average'.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def add_rsi(data, window_length=14):
    """
        Рассчитывает  Индекс относительной силы (Relative Strength Index, RSI) и добавляет его в DataFrame.

        Параметры:
            data (pandas.DataFrame): Данные акций с историческими ценами. Должен содержать столбец 'Close'.
            window_length (int, optional): Размер окна для расчета RSI. По умолчанию 14.

        Возвращает:
            pandas.DataFrame: Исходный DataFrame с добавленным столбцом 'RSI'.
    """
    data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=window_length).rsi()
    return data


def add_macd(data):
    """
       Рассчитывает MACD (Moving Average Convergence Divergence) и добавляет его в DataFrame.

       Параметры:
           data (pandas.DataFrame): Данные акций с историческими ценами. Должен содержать столбец 'Close'.

       Возвращает:
           pandas.DataFrame: Исходный DataFrame с добавленными столбцами:
                             - 'MACD': Значения MACD.
                             - 'MACD_Signal': Линия сигнала MACD.
                             - 'MACD_Hist': Гистограмма MACD.
    """
    macd = ta.trend.MACD(data['Close'])
    data['MACD'] = macd.macd()
    data['MACD_Signal'] = macd.macd_signal()
    data['MACD_Hist'] = macd.macd_diff()
    return data


def add_standard_deviation(data, window_size=20):
    """
        Добавляет стандартное отклонение цен закрытия за указанное окно.

        Параметры:
            data (pandas.DataFrame): Данные акций с историческими ценами. Должен содержать столбец 'Close'.
            window_size (int, optional): Размер окна для расчёта стандартного отклонения. По умолчанию 20.

        Возвращает:
            pandas.DataFrame: Исходный DataFrame с добавленным столбцом 'Standard_Deviation'.
    """
    data['Standard_Deviation'] = data['Close'].rolling(window=window_size).std()
    return data
