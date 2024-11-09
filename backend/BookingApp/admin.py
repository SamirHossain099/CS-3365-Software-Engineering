from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'showtime', 'ticket_count', 'total_price', 'barcode', 'created_at')
    search_fields = ('user__email', 'showtime__movie__title', 'barcode')
    list_filter = ('showtime__movie', 'created_at')
    readonly_fields = ('barcode', 'created_at')
