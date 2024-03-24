import pandas as pd
from spyre import server
import os


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
            "options": [{"label": str(i), "value": str(i)} for i in range(1, 29)],  # Опції для регіонів
            "key": "region",  # Ключ параметра
            "action_id": "update_data",  # Ідентифікатор дії для оновлення даних
        },
        {
            "type": "text",
            "label": "Рік:",
            "value": "2005",
            "key": "year",  # Ключ параметра
            "action_id": "update_data",  # Ідентифікатор дії для оновлення даних
        },
    ]

    # Визначення кнопки для оновлення даних
    controls = [{"type": "button", "label": "Побудувати", "id": "update_data"}]

    # Визначення вкладок
    tabs = ["Plot", "Table"]

    # Визначення вихідних параметрів (графік та таблиця)
    outputs = [
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "output_type": "html",
            "get_html": "getHTML",
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
        data = pd.read_csv(file_path)
        return data
    
    # Фільтрую дані з файлу за рокомі регіоном для виводоу в таблиці
    def getDataForYearAndRegion(self, params, year, region):
        data = self.getData(params)
        filtered_data = data[(data['Indexes'] == region) & (data['Year'] == year)]
        return filtered_data

    # Функція для виведення графіку за регіоном, роком і потрібним рядком
    def getPlot(self, params):
        region = int(params['region'])
        ticker = params['ticker']
        year = int(params['year'])
        data = self.getData(params)
        filtered_data = data[(data['Indexes'] == region) & (data['Year'] == year)]

        plt_obj = filtered_data.plot(x='Week', y=ticker)
        plt_obj.set_ylabel("Значення")
        plt_obj.set_xlabel("Тиждень")
        plt_obj.set_title(f"Графік для регіону {region} у {year} році")
        fig = plt_obj.get_figure()
        return fig
    
    # Вивід таблиці
    def getHTML(self, params):
        year = int(params['year'])
        region = int(params['region'])
        data = self.getDataForYearAndRegion(params, year, region)
        return data.to_html()

if __name__ == '__main__':
    app = SimpleApp()
    app.launch()
