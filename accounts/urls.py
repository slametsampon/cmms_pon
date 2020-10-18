# accounts/urls.py
from django.urls import path
from . import views 

app_name = 'accounts'
urlpatterns = [
    path('', views.AccountsHomeView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('list/', views.CmmsUserListView.as_view(), name='accounts'),
    path('detail/<int:pk>', views.CmmsUserDetailView.as_view(), name='account-detail'),
]
