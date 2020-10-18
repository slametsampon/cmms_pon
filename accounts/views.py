# accounts/views.py
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import CmmsUserCreationForm
from .models import CmmsUser

class AccountsHomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/home.html'

class SignUpView(generic.CreateView):
    form_class = CmmsUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CmmsUserListView(LoginRequiredMixin, generic.ListView):
    #form_class = Wo_search_form
    model = CmmsUser #prinsipnya dengan ini saja sdh cukup, namun kita perlu tambahan info di bawah ini
    template_name = 'accounts/account_list.html'  # Specify your own template name/location

class CmmsUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = CmmsUser #prinsipnya dengan ini saja sdh cukup, namun kita perlu tambahan info di bawah ini
    template_name = 'accounts/account_detail.html'  # Specify your own template name/location
