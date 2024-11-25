from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register_user'),
    path('login/', views.LoginUserView.as_view(), name='login_user'),
    path('all/', views.get_all_users, name='get_all_users'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
]