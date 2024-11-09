from django.urls import path
from . import views

urlpatterns = [
    path('reviews/<int:movie_id>/', views.get_reviews, name='get_reviews'),            # User can get all reviews for a movie
    path('reviews/add/', views.add_review, name='add_review'),          # User can add a review for a movie
    path('reviews/update/<int:review_id>/', views.update_review, name='update_review'), # User can update a review for a movie
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review')  # Admin can delete a review for a movie
]
