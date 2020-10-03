from django.urls import path
from . import views

app_name = 'utility'
urlpatterns = [
    path('', views.UtilityHomeView.as_view(), name='home-utility'),
]

urlpatterns += [  
    path('department/create/', views.DepartmentCreate.as_view(), name='department-create'),
    path('section/create/', views.SectionCreate.as_view(), name='section-create'),
    path('config/import/', views.ImportFileFormView.as_view(), name='config-import'),
]

