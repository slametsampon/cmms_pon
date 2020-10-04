from django.urls import path
from . import views

app_name = 'work_order'
urlpatterns = [  
    path('', views.Work_orderHomeView.as_view(), name='home-work_order'),
    path('list/', views.Work_orderListView.as_view(), name='work_orders'),
    path('detail/<int:pk>', views.Work_orderDetailView.as_view(), name='work_order-detail'),
    path('create/', views.Work_orderCreate.as_view(), name='work_order-create'),
    path('update/<int:pk>/', views.Work_orderUpdate.as_view(), name='work_order-update'),
    path('forward/<int:pk>/', views.Work_orderForward.as_view(), name='work_order-forward'),
    path('complete/<int:pk>/', views.WoCompletion.as_view(), name='work_order-complete'),
    path('instruction/<int:pk>/', views.Wo_instructionCreate.as_view(), name='wo_instruction-create'),
    path('summary/', views.WoSummaryReportView.as_view(), name='work_order-summary'),
    path('report/', views.WoReportView.as_view(), name='work_order-report'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
