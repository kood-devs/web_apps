from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import Article
from .scrape import *

nikkei_category = {
    # 'de': ['search?keyword=国内株式', '国内株式'],  # 左記のようにしたいが…
    'economic': ['economy/economic/', '経済'],
    'monetary': ['economy/monetary/', '金融機関'],
    'politics': ['politics/politics/', '政治'],
    'startups': ['business/startups/', 'スタートアップ'],
    'internet': ['business/internet/', 'ネット・IT'],
    'ai': ['technology/ai/', 'AI'],
    'fintech': ['technology/fintech/', 'フィンテック'],
}


class ArticleList(TemplateView):
    template_name = 'scrape_main.html'
    model = Article

    def get(self, request):
        all_context_list = []
        for category_id, category_content in nikkei_category.items():
            category_path, category_name = category_content
            context_list = []
            article = scrape_nikkei(category_path)
            for key, value in article.items():
                context_list.append({
                    'title': key,
                    'content': value[0],
                    'link': value[1],
                })
            all_context_list.append([category_id, category_name, context_list])
        return render(request, 'scrape_main.html', {'all_context_list': all_context_list, })
