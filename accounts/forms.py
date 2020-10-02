# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CmmsUser

class CmmsUserCreationForm(UserCreationForm):

    class Meta:
        model = CmmsUser
        fields = ('username', 'email')

class CmmsUserChangeForm(UserChangeForm):

    class Meta:
        model = CmmsUser
        fields = ('username', 'email')