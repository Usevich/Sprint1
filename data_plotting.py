import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go


def create_and_save_plot(data, ticker, style='', filename=None):
    """
    Создает график с тремя подграфиками (цена акций со скользящей средней, RSI, MACD)
    и сохраняет его в файл.

    :param data: DataFrame. Таблица с данными акций. Ожидаются следующие столбцы:
                 - 'Close': цены закрытия,
                 - 'Moving_Average': скользящая средняя,
                 - 'Standard_Deviation': стандартное отклонение,
                 - 'RSI': индекс относительной силы,
                 - 'MACD', 'MACD_Signal', 'MACD_Hist': метрики для MACD.
    :param ticker: str. Символ акции (например, 'AAPL').
    :param style: str. Название стиля графика matplotlib (по умолчанию 'classic').
    :param filename: str. Имя файла, в который будет сохранен график
     (по умолчанию используется '{ticker}_stock_price_chart_with_indicators.png').

    """
    if style == '':
        style = 'classic'

    plt.style.use(style)  # Применяем выбранный стиль
    plt.figure(figsize=(14, 10))
    # Подграфик для цены и скользящей средней
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(data.index, data['Close'], label='Close Price')
    ax1.plot(data.index, data['Moving_Average'], label='Moving Average')
    ax1.plot(data.index, data['Standard_Deviation'], label='Стандартное отклонение', color='green', linestyle='--')
    ax1.set_title(f"{ticker} Цена акций и средние")
    ax1.set_xlabel("Дата")
    ax1.set_ylabel("Цена")
    ax1.legend(framealpha=0.5, loc='best')

    # Подграфик для RSI
    ax2 = plt.subplot(3, 1, 2)
    ax2.plot(data.index, data['RSI'], label='RSI')
    ax2.set_title("Индекс относительной силы (RSI)")
    ax2.set_xlabel("Дата")
    ax2.set_ylabel("RSI")
    ax2.axhline(70, color='red', linestyle='--', alpha=0.5, label="Overbought")
    ax2.axhline(30, color='green', linestyle='--', alpha=0.5, label="Oversold")
    ax2.legend(framealpha=0.5, loc='best')

    # Подграфик для MACD
    ax3 = plt.subplot(3, 1, 3)
    ax3.plot(data.index, data['MACD'], label='MACD')
    ax3.plot(data.index, data['MACD_Signal'], label='Signal Line')
    ax3.bar(data.index, data['MACD_Hist'], label='MACD Histogram', color='gray')
    ax3.set_title("MACD")
    ax3.set_xlabel("Дата")
    ax3.set_ylabel("MACD")
    ax3.legend(framealpha=0.5, loc='best')

    if filename is None:
        filename = f"{ticker}_stock_price_chart_with_indicators.png"

    plt.tight_layout()
    plt.savefig(filename)
    print(f"График с индикаторами сохранен как {filename}")
    # plt.show()


def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия акций за указанный период.

    :param data: DataFrame. Таблица с данными акций. Ожидается столбец 'Close' с ценами закрытия.

    """
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


def create_interactive_plot(data, ticker):
    """
    Создает и отображает интерактивный график цен закрытия с использованием библиотеки plotly.

    :param data: DataFrame. Таблица с данными акций. Ожидается столбец 'Close' с ценами закрытия.
    :param ticker: str. Символ акции (например, 'AAPL').

    """
    # Добавляем трассировку данных 'Close'
    trace = go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Цена закрытия')

    # Создаем макет графика
    layout = go.Layout(
        title=f'Интерактивный график для {ticker}',
        xaxis=dict(title='Дата'),
        yaxis=dict(title='Цена закрытия'),
        hovermode='x'
    )

    # Строим и выводим график
    fig = go.Figure(data=[trace], layout=layout)
    fig.show()
