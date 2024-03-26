import pandas as pd
from spyre import server
import os
import datetime as dt

class SimpleApp(server.App):
    title = "Data visualization"  # Заголовок додатку

    # Визначення вхідних параметрів для користувача
    inputs = [
        {
            "type": "dropdown",
            "label": "Дані",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"},
            ],
            "key": "ticker",  # Ключ параметра
            "action_id": "update_data",  # Ідентифікатор дії для оновлення даних
        },
        {
            "type": "dropdown",
            "label": "Область",
            "options": [{"label": "Вінницька", "value": "1"},
                        {"label": "Волинська", "value": "2"},
                        {"label": "Дніпропетровська", "value": "3"},
                        {"label": "Донецька", "value": "4"},
                        {"label": "Житомирська", "value": "5"},
                        {"label": "Закарпатська", "value": "6"},
                        {"label": "Запорізька", "value": "7"},
                        {"label": "Івано-Франківська", "value": "8"},
                        {"label": "Київська", "value": "9"},
                        {"label": "Кіровоградська", "value": "10"},
                        {"label": "Луганська", "value": "11"},
                        {"label": "Львівська", "value": "12"},
                        {"label": "Миколаївська", "value": "13"},
                        {"label": "Одеська", "value": "14"},
                        {"label": "Полтавська", "value": "15"},
                        {"label": "Рівенська", "value": "16"},
                        {"label": "Сумська", "value": "17"},
                        {"label": "Тернопільська", "value": "18"},
                        {"label": "Харківська", "value": "19"},
                        {"label": "Херсонська", "value": "20"},
                        {"label": "Хмельницька", "value": "21"},
                        {"label": "Черкаська", "value": "22"},
                        {"label": "Чернівецька", "value": "23"},
                        {"label": "Чернігівська", "value": "24"},
                        {"label": "Республіка Крим", "value": "25"},
                        {"label": "Севостопель", "value": "26"},
                        {"label": "КиЇв", "value": "27"}],  # Опції для регіонів
            "key": "region",  # Ключ параметра
            "action_id": "update_data",  # Ідентифікатор дії для оновлення даних
        },
        {
            "type": "text",
            "label": "Рік:",
            "value": "2005",
            "key": "start_year",  # Ключ параметра
            "action_id": "update_data",  # Ідентифікатор дії для оновлення даних
        },
        {
            "type": "text",
            "label": "Рік:",
            "value": "2005",
            "key": "end_year",  # Ключ параметра
            "action_id": "update_data",  # Ідентифікатор дії для оновлення даних
        },
         {
            "type": 'text',
            "label": 'Week min',
            "key": 'week_min',
            "value": '1',
            "action_id": "update_data"
        },

        {
            "type": 'text',
            "label": 'Week max',
            "key": 'week_max',
            "value": '52',
            "action_id": "update_data"
        }
    ]

    # Визначення кнопки для оновлення даних
    controls = [{"type": "hidden", "id": "update_data"}]

    # Визначення вкладок
    tabs = ["Plot", "Table"]

    # Визначення вихідних параметрів (графік та таблиця)
    outputs = [
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        },
        {
            "type": "plot",
            "id": "plot_id",
            "control_id": "update_data",
            "tab": "Plot",
        },
    ]

    # Завантажую дані з CSV-файлу
    def getData(self, params):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'data.csv')
        df = pd.read_csv(file_path)
        return df
    
    def getTable(self, params):
        df = self.getData(params)
        region = int(params['region'])
        start_year = int(params['start_year'])
        end_year = int(params['end_year'])
        week_min = int(params['week_min'])
        week_max = int(params['week_max'])
        if week_max > 52 or week_min > 52:
            return pd.DataFrame({'message': ['Будь ласка, введіть значення для Week max або Week min менше або рівне 52.']})
        if week_max < week_min and start_year >= end_year:
            return pd.DataFrame({'message': ['Будь ласка, введіть правильні дані для Week min і Week max.']})
        if end_year - start_year > 1:
            data = df[(df['Indexes'] == region)]
            data = data[((data['Year'] == start_year) & (data['Week'] >= week_min)) |
                    ((data['Year'] == end_year) & (data['Week'] <= week_max)) |
                    ((data['Year'] > start_year) & (data['Year'] < end_year))]
        elif start_year == end_year:
            data = df[(df['Indexes'] == region) & (df['Year'] == start_year) & df['Week'].between(week_min, week_max)]
        else:
        # В іншому випадку враховуємо тільки вибрані роки
            data = df[(df['Indexes'] == region)]
            data = data[((data['Year'] == start_year) & (data['Week'] >= week_min)) |
                    ((data['Year'] == end_year) & (data['Week'] <= week_max))]
        columns = ['Year', 'Week', params['ticker'], 'Indexes']
        return data.loc[:, columns]


    # Функція для виведення графіку за регіоном, роком і потрібним рядком
    def getPlot(self, params):
        region = int(params['region'])
        ticker = params['ticker']
        start_year = int(params['start_year'])
        end_year = int(params['end_year'])
        week_min = int(params['week_min'])
        week_max = int(params['week_max'])
        df = self.getData(params)
        if end_year - start_year > 1:
            data = df[(df['Indexes'] == region)]
            data = data[((data['Year'] == start_year) & (data['Week'] >= week_min)) |
                    ((data['Year'] == end_year) & (data['Week'] <= week_max)) |
                    ((data['Year'] > start_year) & (data['Year'] < end_year))]
        elif end_year == start_year:
            data = df[(df['Indexes'] == region) & (df['Year'] == start_year) & df['Week'].between(week_min, week_max)]
        else:
            data = df[(df['Indexes'] == region)]
            data = data[((data['Year'] == start_year) & (data['Week'] >= week_min)) |
                    ((data['Year'] == end_year) & (data['Week'] <= week_max))]
        data['Date'] = pd.to_datetime(data.Year.astype(str), format='%Y') + \
             pd.to_timedelta(data.Week.mul(7).astype(str) + ' days')
        
        plt_obj = data.plot(x='Date', y=ticker)
        plt_obj.set_ylabel("NOAA дані")
        plt_obj.set_xlabel("Тиждень")
        plt_obj.set_title(f"Графік для регіону {region} за період з {week_min} {start_year} по {week_max} {end_year}")
        plot = plt_obj.get_figure()
        return plot

if __name__ == '__main__':
    app = SimpleApp()
    app.launch()