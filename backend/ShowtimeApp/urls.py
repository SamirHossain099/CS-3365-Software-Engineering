from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowtimeViewSet

router = DefaultRouter()
router.register(r'showtimes', ShowtimeViewSet, basename='showtime')

urlpatterns = [
    path('', include(router.urls)),
]
