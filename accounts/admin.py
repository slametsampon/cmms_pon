# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CmmsUserCreationForm, CmmsUserChangeForm
from .models import CmmsUser

class CmmsUserAdmin(UserAdmin):
    add_form = CmmsUserCreationForm
    form = CmmsUserChangeForm
    model = CmmsUser
    list_display = ['email', 'username',]

admin.site.register(CmmsUser, CmmsUserAdmin)
