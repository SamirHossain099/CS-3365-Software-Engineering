from django.contrib import admin
from .models import Movie
# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre', 'director', 'imdb_rating')
    list_filter = ('genre', 'director', 'release_date')