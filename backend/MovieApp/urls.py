from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.get_movie, name='get_movies'),                       #User can get all movies
    path('movies/add/', views.add_movie, name='add_movie'),                     #Admin can add a movie
    path('movies/update/', views.update_movie, name='update_movie'),            #Admin can update a movie
    path('movies/delete/', views.delete_movie, name='delete_movie'),            #Admin can delete a movie
    path('movies/details/', views.get_movie_details, name='get_movie_details'), #User can get details of a movie
    path('movies/update_rating/', views.update_rating, name='update_rating')    #Admin can update the rating of a movie
]