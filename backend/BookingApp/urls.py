# BookingApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),  # Create a booking
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),  # Cancel a booking
    path('details/<int:booking_id>/', views.get_booking_details, name='get_booking_details'),  # Get booking details
    path('user/<int:user_id>/tickets/', views.get_user_tickets, name='get_user_tickets'),  # Add this line
]
