from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.get_movies, name='get_movies'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/update/', views.update_movie, name='update_movie'),
    path('movies/delete/', views.delete_movie, name='delete_movie'),
    path('movies/details/', views.get_movie_details, name='get_movie_details'),
    path('movies/update_rating/', views.update_rating, name='update_rating')
]