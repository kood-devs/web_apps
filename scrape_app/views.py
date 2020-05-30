from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import Article
from .scrape import *

nikkei_category = {
    # '速報': 'news/category/',
    '経済': 'economy/economic/',
    '金融': 'economy/monetary/',
    'インターネット': 'business/internet/',
    'スタートアップ': 'business/startups/',
}


class ArticleList(TemplateView):
    template_name = 'scrape_main.html'
    model = Article

    def get(self, request):
        all_context_list = []
        for category_name, category_path in nikkei_category.items():
            context_list = []
            article = scrape_nikkei(category_path)
            for key, value in article.items():
                context_list.append({
                    'title': key,
                    'content': value[0],
                    'link': value[1],
                })
            # all_context_list.append(context_list)
            all_context_list.append([category_name, context_list])
        return render(request, 'scrape_main.html', {'all_context_list': all_context_list,})
