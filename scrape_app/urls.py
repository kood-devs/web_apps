from django.urls import path
from .views import ArticleList

app_name = 'scrape_app'
urlpatterns = [
    path('scrape_main/', ArticleList.as_view(), name='scrape_main'),
]
