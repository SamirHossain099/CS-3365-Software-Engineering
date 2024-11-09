from django.contrib import admin
from .models import Showtime

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater_location', 'show_date', 'show_time', 'ticket_price')
    search_fields = ('movie__title', 'theater_location')
    list_filter = ('theater_location', 'show_date')
