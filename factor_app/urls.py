from django.urls import path
from .views import MainForm, UpdateForm

app_name = 'factor_app'
urlpatterns = [
    path('factor_main/', MainForm.as_view(), name='factor_main'),
    path('factor_update/<int:pk>', UpdateForm.as_view(), name='factor_update'),
]
