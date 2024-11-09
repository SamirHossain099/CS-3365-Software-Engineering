from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.get_movie_list_api, name='get_movies'),                        # User can get all movies
    path('movies/add/', views.add_movie, name='add_movie'),                              # Admin can add a movie
    path('movies/update/<int:movie_id>/', views.update_movie, name='update_movie'),      # Admin can update a movie
    path('movies/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),      # Admin can delete a movie
    path('movies/details/<int:movie_id>/', views.get_movie_reviews_api, name='get_movie_details'), # User can get details of a movie
    path('movies/update_rating/', views.update_rating, name='update_rating')             # Admin can update the rating of a movie
]