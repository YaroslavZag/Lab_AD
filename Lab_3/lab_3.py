import pandas as pd
from spyre import server
import os


class SimpleApp(server.App):
    title = "Data vizualization"

    inputs = [
        {
            "type": "dropdown",
            "label": "Дані",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"},
            ],
            "key": "ticker",
            "action_id": "update_data",
        },
        {
            "type": "dropdown",
            "label": "Область",
            "options": [{"label": str(i), "value": str(i)} for i in range(1, 29)],
            "key": "region",
            "action_id": "update_data",
        },
        {
            "type": "text",
            "label": "Рік:",
            "value": "2005",
            "key": "year",
            "action_id": "update_data",
        },
    ]

    controls = [{"type": "button", "label": "Побудувати", "id": "update_data"}]

    tabs = ["Plot", "Table"]

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

    def getData(self, params):
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'data.csv')
        data = pd.read_csv(file_path)
        return data
    
    def getDataForYearAndRegion(self, params, year, region):
        data = self.getData(params)
        filtered_data = data[(data['Indexes'] == region) & (data['Year'] == year)]
        return filtered_data

    def getPlot(self, params):
        region = int(params['region'])
        ticker = params['ticker']
        year = int(params['year'])  # Перетворення рядка на ціле число
        data = self.getData(params)
        filtered_data = data[(data['Indexes'] == region) & (data['Year'] == year)]

        plt_obj = filtered_data.plot(x='Week', y=ticker)
        plt_obj.set_ylabel("Значення")
        plt_obj.set_xlabel("Тиждень")
        plt_obj.set_title(f"Графік для регіону {region} у {year} році")
        fig = plt_obj.get_figure()
        return fig
    
    def getHTML(self, params):
        year = int(params['year'])  # Перетворення рядка на ціле число
        region = int(params['region'])  # Перетворення рядка на ціле число
        data = self.getDataForYearAndRegion(params, year, region)
        return data.to_html()

if __name__ == '__main__':
    app = SimpleApp()
    app.launch()
