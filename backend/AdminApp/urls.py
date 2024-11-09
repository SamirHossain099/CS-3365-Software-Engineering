from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.AdminLogListView.as_view(), name='admin-logs-list'),
    path('log/create/', views.AdminLogCreateView.as_view(), name='admin-log-create'),
    path('log/<int:admin_id>/', views.AdminLogsByAdminView.as_view(), name='admin-logs-by-admin'),
]
