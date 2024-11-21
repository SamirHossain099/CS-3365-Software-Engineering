from django.contrib import admin
from .models import Showtime

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('showtime_id', 'movie', 'show_date', 'show_time', 'ticket_price', 'available_seats')
    search_fields = ('movie__title', 'show_date')
    list_filter = ('movie', 'show_date')
    readonly_fields = ('showtime_id',)
