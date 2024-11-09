from django.urls import path
from . import views

urlpatterns = [
    path('viewmovies/', views.get_movie_list, name='get_movies'),
    path('add/', views.add_movie, name='add_movie'),
    path('update/<int:movie_id>/', views.update_movie, name='update_movie'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('details/<int:movie_id>/', views.get_movie_reviews, name='get_movie_details'),
    path('update_rating/', views.update_rating, name='update_rating')
]