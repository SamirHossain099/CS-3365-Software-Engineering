from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'showtime', 'ticket_count', 'total_price', 'created_at')
    search_fields = ('user__username', 'showtime__movie__title', 'barcode')
    list_filter = ('created_at',)
