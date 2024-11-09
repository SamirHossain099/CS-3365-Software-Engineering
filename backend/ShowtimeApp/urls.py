from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_id>/list/', views.showtime_list, name='showtime_list'),  # List showtimes for a movie
    path('<int:movie_id>/create/', views.create_showtime, name='create_showtime'),  # Create a new showtime
    path('delete/<int:showtime_id>/', views.delete_showtime, name='delete_showtime'),  # Delete a showtime
]
