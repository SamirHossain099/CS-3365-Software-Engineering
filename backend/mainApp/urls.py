# urls for the mainApp
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('theaters/', views.theaters, name='theaters'),
    path('movies/', views.movies, name='movies'),
    path('purchases/', views.receipts, name='purchases'),
]
