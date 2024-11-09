from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.get_reviews, name='get_reviews'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('reviews/update/', views.update_review, name='update_review')
]
