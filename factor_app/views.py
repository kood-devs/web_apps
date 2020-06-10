from django.shortcuts import render
from django.views.generic import TemplateView


class MainForm(TemplateView):
    template_name = 'factor_main.html'
