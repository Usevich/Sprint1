import data_download as dd
import data_plotting as dplt
from datetime import datetime

def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL "
          "(Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л,"
          " с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

    # Получите ввод пользователя о том, какой способ времени он предпочитает
    choice = input("Хотите использовать предустановленный период (Введите 'p') или указать конкретные даты (Введите 'd')? ")

    if choice.lower() == 'd':
        # Получить и проверить даты
        while True:
            start_date = input("Введите дату начала (в формате ГГГГ-ММ-ДД): ")
            end_date = input("Введите дату окончания (в формате ГГГГ-ММ-ДД): ")
            try:
                # Проверка правильности дат
                start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
                end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
                if start_datetime > end_datetime:
                    print("Дата начала должна быть сраньше даты окончания. Попробуйте еще раз.")
                else:
                    break
            except ValueError:
                print("Некорректный формат даты. Попробуйте еще раз.")
        # Fetch stock data with specific dates
        stock_data = dd.fetch_stock_data(ticker, start_date=start_date, end_date=end_date)

    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        # Fetch stock data with given period
        stock_data = dd.fetch_stock_data(ticker, period=period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)
    dplt.calculate_and_display_average_price(stock_data)
    # Plot the data
    stock_data = dd.add_rsi(stock_data)
    stock_data = dd.add_macd(stock_data)
    dplt.create_and_save_plot(stock_data, ticker)
    dplt.notify_if_strong_fluctuations(stock_data, 10)  # Проверяет колебания свыше 10%
    dplt.export_data_to_csv(stock_data, f'{ticker}.csv')  # Экспортирует данные в формат CSV


if __name__ == "__main__":
    main()
