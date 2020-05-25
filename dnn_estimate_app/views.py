import os

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .models import LearningModel
from .dnn_estimator import *


class MainForm(ListView):
    template_name = 'dnn_est_main.html'
    model = LearningModel


class DetailForm(DetailView):
    template_name = 'dnn_est_detail.html'
    model = LearningModel


class SetParam(CreateView):
    template_name = 'dnn_est_set.html'
    model = LearningModel
    fields = ('title', 'train_start', 'train_end',
              'test_start', 'test_end', 'epoch', 'batch_size')
    success_url = reverse_lazy('dnn_estimate_app:dnn_est_main')


class DeleteParam(DeleteView):
    template_name = 'dnn_est_delete.html'
    model = LearningModel
    success_url = reverse_lazy('dnn_estimate_app:dnn_est_main')


def learn_dnn_model(request, pk):
    # learn individual model
    params = LearningModel.objects.get(pk=pk)
    result = learn_dnn(
        params.train_start, params.train_end, params.test_start, params.test_end, params.epoch, params.batch_size, params.title)
    params.train_acc, params.test_acc = result
    params.images = '{}.jpg'.format(params.title)
    params.save()
    return redirect('dnn_estimate_app:dnn_est_main')
