from django.urls import path
from .views import MainForm, DetailForm, SetParam, DeleteParam, learn_dnn_model

app_name = 'dnn_estimate_app'
urlpatterns = [
    path('dnn_est_main/', MainForm.as_view(), name='dnn_est_main'),
    path('dnn_est_detail/<int:pk>', DetailForm.as_view(), name='dnn_est_detail'),
    path('dnn_est_set/', SetParam.as_view(), name='dnn_est_set'),
    path('dnn_est_delete/<int:pk>', DeleteParam.as_view(), name='dnn_est_delete'), 
    path('dnn_est_learn/<int:pk>', learn_dnn_model, name='dnn_est_learn'),    
]
