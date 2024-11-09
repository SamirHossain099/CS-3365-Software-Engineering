from django.urls import path
from .views import (
    BookingListView,
    BookingCreateView,
    BookingsByUserView,
    BookingCancelView
)

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('user/<int:user_id>/', BookingsByUserView.as_view(), name='bookings-by-user'),
    path('cancel/<int:booking_id>/', BookingCancelView.as_view(), name='booking-cancel'),
]
