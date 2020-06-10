import os

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import MarketForecastModel
from .model_forecast import *

asset_class = {
    'DE': '国内株式',
    'DB': '国内債券',
    'FE': '先進国株式',
    'FB': '先進国債券',
}


class MainForm(TemplateView):
    template_name = 'forecast_main.html'
    model = MarketForecastModel

    def get(self, request):
        contents = self.forecast_market()
        index_data = get_recent_index()
        index_cols = index_data.columns.to_list()
        index_cols = ['Date', *index_cols]
        return render(request, 'forecast_main.html', {'contents': contents, 'index_data': index_data, 'index_cols': index_cols, })

    @staticmethod
    def forecast_market():
        contents = []
        for asset_id, asset_name in asset_class.items():
            obj, _ = MarketForecastModel.objects.get_or_create(title=asset_id)
            contents.append([asset_name, obj.model_defined_date, obj.weather])
        return contents

    # def get(self, request):
    #     contents = self.forecast_market()
    #     index_data = get_recent_index()
    #     index_cols = index_data.columns.to_list()
    #     index_cols = ['Date', *index_cols]
    #     return render(request, 'forecast_main.html', {'contents': contents, 'index_data': index_data, 'index_cols': index_cols, })
    #
    # @staticmethod
    # def forecast_market():
    #     # 天気予報
    #     contents = []
    #     for asset_id, asset_name in asset_class.items():
    #         if asset_id == 'DE':
    #             prediction_date, result = run_forecast(
    #                 asset_id, 'binomial logit', 2600)
    #             result = 'sunny' if result == 1 else 'rainy'
    #             contents.append([asset_name, prediction_date, result])
    #         else:
    #             contents.append([asset_name, prediction_date, 'cloudy'])
    #     return contents


def update_form(request):
    for title_key in asset_class.keys():
        # 取得
        obj, _ = MarketForecastModel.objects.get_or_create(title=title_key)
        # 更新
        if obj.title == 'DE':
            prediction_date, result = run_forecast(
                title_key, obj.forecast_model, obj.train_num)
            result = 'sunny' if result == 1 else 'rainy'
        else:
            result = 'cloudy'
        # 設定
        obj.model_defined_date = prediction_date
        obj.weather = result
        obj.save()
    return redirect('forecast_app:forecast_main')
