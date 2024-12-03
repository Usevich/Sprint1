import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None):
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")


def calculate_and_display_average_price(data):

    # Вычисляет и отображает среднюю цену закрытия акций за заданный период.

    # data: DataFrame, содержащий данные о цене акций.
    if 'Close' not in data:
        print("Колонка 'Close' отсутствует в предоставленном датафрейме.")
        return

    # Вычисление средней цены закрытия
    average_price = data['Close'].mean()

    # Вывод результата в консоль
    print(f"Средняя цена закрытия акций за указанный период: {average_price:.2f}")

def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет пользователя, если колебания цен превышают заданный процент.

    :param data: DataFrame, содержащий данные о цене акций.
    :param threshold: Порог в процентах, который необходимо превысить для уведомления.
    """
    if 'Close' not in data:
        print("Колонка 'Close' отсутствует в предоставленном датафрейме.")
        return

    # Находим минимальные и максимальные цены закрытия
    min_price = data['Close'].min()
    max_price = data['Close'].max()

    # Вычисляем процентовое изменение
    percentage_change = ((max_price - min_price) / min_price) * 100

    # Проверяем, превышает ли изменение порог и уведомляем пользователя
    if percentage_change > threshold:
        print(f"Внимание: Цена акций колебалась более чем на {threshold}% (фактически {percentage_change:.2f}%)!")
    else:
        print(f"Изменения в пределах допустимого порога. Фактическое изменение: {percentage_change:.2f}%.")


