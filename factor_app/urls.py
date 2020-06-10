from django.urls import path
from .views import MainForm

app_name = 'factor_app'
urlpatterns = [
    path('factor_main/', MainForm.as_view(), name='factor_main'),
]
