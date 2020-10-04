from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.
class ReportingHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'reporting/home.html'

