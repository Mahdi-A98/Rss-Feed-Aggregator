# In the name of GOD 
from django.urls import path
from .views import LikeView, CommentView, AddToPlaylistView

app_name="feedback"
urlpatterns = [
    path("like/", LikeView.as_view(),name='like'),
    path("comment/", CommentView.as_view(),name='comment'),
    path("bookmark/", AddToPlaylistView.as_view(),name='bookmark'),
]