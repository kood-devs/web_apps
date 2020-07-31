from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from .models import PortfolioModel
from .factor_analysis import *


class MainForm(TemplateView):
    template_name = 'factor_main.html'
    model = PortfolioModel

    def get(self, request):
        # モデルを作成 or 作成済みモデルの取得
        obj, _ = PortfolioModel.objects.get_or_create(title='登録ポートフォリオ')
        obj.save()

        port_weight = []
        port_weight.append(obj.weight_DB)
        port_weight.append(obj.weight_DE)
        port_weight.append(obj.weight_FB)
        port_weight.append(obj.weight_FE)
        port_weight.append(obj.weight_EB)
        port_weight.append(obj.weight_EE)
        port_weight.append(obj.weight_DR)
        port_weight.append(obj.weight_FR)

        # ファクター
        factor_index = get_factor_return(is_cum_index=True, num_of_days=90)
        factor_index_col = factor_index.columns.to_list()

        # 資産
        asset_index = get_asset_return(is_cum_index=True, num_of_days=90)
        asset_index_col = asset_index.columns.to_list()

        # 個別資産リターンファクター分解
        factor_decomp, decomp_date = get_factor_analysis()
        factor_decomp_col = factor_decomp.columns.to_list()

        contents = {
            # port data
            'port_weight': port_weight,
            # factor data
            'factor_index': factor_index,
            'factor_index_col': factor_index_col,
            'asset_index': asset_index,
            'asset_index_col': asset_index_col,
            'factor_decomp': factor_decomp,
            'factor_decomp_col': factor_decomp_col,
            'decomp_date': decomp_date,
        }
        return render(request, 'factor_main.html', contents)


class UpdateForm(UpdateView):
    template_name = 'factor_update.html'
    model = PortfolioModel
    fields = (
        'weight_DB',
        'weight_DE',
        'weight_FB',
        'weight_FE',
        'weight_EB',
        'weight_EE',
        'weight_DR',
        'weight_FR',
    )
    success_url = reverse_lazy('factor_main')
