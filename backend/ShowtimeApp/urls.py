from django.urls import path
from .views import (
    ShowtimeListView,
    ShowtimeCreateView,
    ShowtimesByMovieView,
    ShowtimesByTheaterView,
    ShowtimeUpdateView,
    ShowtimeDeleteView
)

urlpatterns = [
    path('', ShowtimeListView.as_view(), name='showtime-list'),
    path('create/', ShowtimeCreateView.as_view(), name='showtime-create'),
    path('movie/<int:movie_id>/', ShowtimesByMovieView.as_view(), name='showtimes-by-movie'),
    path('theater/<str:theater_location>/', ShowtimesByTheaterView.as_view(), name='showtimes-by-theater'),
    path('update/<int:showtime_id>/', ShowtimeUpdateView.as_view(), name='showtime-update'),
    path('delete/<int:showtime_id>/', ShowtimeDeleteView.as_view(), name='showtime-delete'),
]
