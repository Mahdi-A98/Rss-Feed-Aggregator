from django.urls import path, include
from . import views
app_name='account'
urlpatterns = [
    path('refresh_token/', views.RefreshTokenView.as_view(), name='refresh_token' ),
    path('register/', views.RegisterView.as_view(), name='register' ),
    path('login/', views.LoginView.as_view(), name='login' ),
    path('logout/', views.LogoutView.as_view(), name='logout' ),
    path('profile/', views.ProfileView.as_view(), name='profile' ),
]
