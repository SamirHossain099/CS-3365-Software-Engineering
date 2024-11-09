from django.urls import path
from .views import BookingListView, BookingCreateView, BookingCancelView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('cancel/<int:booking_id>/', BookingCancelView.as_view(), name='booking-cancel'),
]
