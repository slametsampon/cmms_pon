# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CmmsUserCreationForm, CmmsUserChangeForm
from .models import CmmsUser, Mode, Category, Department, Section, Action

@admin.register(CmmsUser)
class CmmsUserAdmin(UserAdmin):
    add_form = CmmsUserCreationForm
    form = CmmsUserChangeForm
    model = CmmsUser
    list_display = ('username','section','forward_path', 'reverse_path', 'actions')
    list_filter = ('section', 'username')
    fieldsets = (
        (None, {
            'fields': ('username',  'section')
        }),
        ('Approval Path', {
            'fields': ('forward_path', 'reverse_path', 'actions')
        }),
        ('Groups', {
            'fields': ('groups',)
        }),
    )
    
class ActionInline(admin.TabularInline):
    model = Action

# Register the Admin classes for Mode using the decorator
@admin.register(Mode)
class ModeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    inlines = [
        ActionInline,
    ]

# Register the Admin classes for Category using the decorator
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    inlines = [
        ActionInline,
    ]

# Register the Admin classes for Action using the decorator
@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('name','mode','description')
    list_filter = ('name','mode','description')

class SectionInline(admin.TabularInline):
    model = Section

# Register the Admin classes for Department using the decorator
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'initial','description')
    list_filter = ('name', 'initial','description')
    inlines = [
        SectionInline,
    ]

# Register the Admin classes for Section using the decorator
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')
        
