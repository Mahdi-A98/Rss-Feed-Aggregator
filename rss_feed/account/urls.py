from django.urls import path, include
from .views import ObtainTokenView
app_name='account'
urlpatterns = [
    path('token/', ObtainTokenView.as_view(), name='token' ),
]
