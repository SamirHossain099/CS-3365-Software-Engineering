from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:showtime_id>/', views.create_booking, name='create_booking'),
    path('detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
]
