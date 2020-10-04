from django.urls import path
from . import views

app_name = 'pm_pdm'
urlpatterns = [
    path('', views.Pm_pdmHomeView.as_view(), name='home'),
]
