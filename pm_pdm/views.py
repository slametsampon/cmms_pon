from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.

class Pm_pdmHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'pm_pdm/home.html'
