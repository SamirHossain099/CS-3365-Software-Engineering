from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price', 'barcode', 'created_at')
    list_display = ('booking_id', 'user', 'showtime', 'ticket_count', 'total_price', 'created_at')
    search_fields = ('booking_id', 'user__email', 'showtime__movie__title')
