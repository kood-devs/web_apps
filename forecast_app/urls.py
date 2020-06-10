from django.urls import path
from .views import MainForm, update_form

app_name = 'forecast_app'
urlpatterns = [
    path('forecast_main/', MainForm.as_view(), name='forecast_main'),
    path('forecast_update/', update_form, name='forecast_update'),
]
