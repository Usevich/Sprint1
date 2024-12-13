import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, filename=None):
    plt.figure(figsize=(14, 10))

    # Подграфик для цены и скользящей средней
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(data.index, data['Close'], label='Close Price')
    ax1.plot(data.index, data['Moving_Average'], label='Moving Average')
    ax1.set_title(f"{ticker} Цена акций и средние")
    ax1.set_xlabel("Дата")
    ax1.set_ylabel("Цена")
    ax1.legend()

    # Подграфик для RSI
    ax2 = plt.subplot(3, 1, 2)
    ax2.plot(data.index, data['RSI'], label='RSI')
    ax2.set_title("Индекс относительной силы (RSI)")
    ax2.set_xlabel("Дата")
    ax2.set_ylabel("RSI")
    ax2.axhline(70, color='red', linestyle='--', alpha=0.5, label="Overbought")
    ax2.axhline(30, color='green', linestyle='--', alpha=0.5, label="Oversold")
    ax2.legend()

    # Подграфик для MACD
    ax3 = plt.subplot(3, 1, 3)
    ax3.plot(data.index, data['MACD'], label='MACD')
    ax3.plot(data.index, data['MACD_Signal'], label='Signal Line')
    ax3.bar(data.index, data['MACD_Hist'], label='MACD Histogram', color='gray')
    ax3.set_title("MACD")
    ax3.set_xlabel("Дата")
    ax3.set_ylabel("MACD")
    ax3.legend()

    if filename is None:
        filename = f"{ticker}_stock_price_chart_with_indicators.png"

    plt.tight_layout()
    plt.savefig(filename)
    print(f"График с индикаторами сохранен как {filename}")


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


def export_data_to_csv(data, filename):
    """
    Экспортирует данные акций в CSV файл.

    :param data: DataFrame, содержащий данные о цене акций.
    :param filename: Имя файла для сохранения.
    """
    if not isinstance(data, pd.DataFrame):
        print("Предосталенная информация не является DataFrame.")
        return

    try:
        data.to_csv(filename, index=False)
        print(f"Данные успешно экспортированы в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
