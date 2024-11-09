from django.contrib import admin
from .models import Movie
# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genre', 'director', 'imdb_rating')
    search_fields = ('title', 'genre', 'director')
    list_filter = ('genre', 'director', 'release_date')