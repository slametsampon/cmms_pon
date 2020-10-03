# accounts/urls.py
from django.urls import path
from .views import SignUpView
# Use include() to add paths from the catalog application 
from django.urls import include

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
