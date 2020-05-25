from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import Article
from .scrape import *

class ArticleList(TemplateView):
    template_name = 'scrape_main.html'
    model = Article

    def get(self, request):
        article = main_scrape()
        context_list = []
        for key, value in zip(article.keys(), article.values()):
            context_list.append({
                'title': key,
                'content': value[0],
                'link': value[1],
            })
        return render(request, 'scrape_main.html', {'context_list': context_list, })
