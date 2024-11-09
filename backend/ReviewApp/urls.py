from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_id>/submit/', views.submit_review, name='submit_review'),  # Submit a review for a movie
    path('<int:movie_id>/reviews/', views.movie_reviews, name='movie_reviews'),  # View all reviews for a movie
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),  # Delete a review (admin only)
]
