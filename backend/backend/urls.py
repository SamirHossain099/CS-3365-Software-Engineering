"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include('BookingApp.urls')),     # Include BookingApp URLs
    path('showtimes/', include('ShowtimeApp.urls')),  # Include ShowtimeApp URLs
    path('reviews/', include('ReviewApp.urls')),      # Include ReviewApp URLs
    path('users/', include('UserApp.urls')),    # Update this line
    path('adminLog/', include('AdminApp.urls')),         # Include AdminApp URLs
    path('movies/', include('MovieApp.urls')),        # Include MovieApp URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Add this line
