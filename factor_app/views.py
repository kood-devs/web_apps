from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .factor_analysis import *


class MainForm(TemplateView):
    template_name = 'factor_main.html'

    def get(self, request):
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
            'factor_index': factor_index,
            'factor_index_col': factor_index_col,
            'asset_index': asset_index,
            'asset_index_col': asset_index_col,
            'factor_decomp': factor_decomp,
            'factor_decomp_col': factor_decomp_col,
            'decomp_date': decomp_date,
        }
        return render(request, 'factor_main.html', contents)
