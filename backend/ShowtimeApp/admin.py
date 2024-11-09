from django.contrib import admin
from .models import Showtime

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('showtime_id', 'movie', 'theater_location', 'show_date', 'show_time', 'ticket_price', 'available_seats')
    search_fields = ('movie__title', 'theater_location')
    list_filter = ('movie', 'show_date', 'theater_location')
    readonly_fields = ('showtime_id',)
