# In the name of GOD 
from django.urls import path
from .views import PodcastListView, EpisodeListView, AddPodcastView,  UpdatePodcastView, AddPodcastUrlView

app_name="podcast"
urlpatterns = [
    path("podcasts/", PodcastListView.as_view(), name="podcasts"),
    path('episodes/', EpisodeListView.as_view(), name='episode'),
    path("add_podcast_url/", AddPodcastUrlView.as_view(), name="add_podcast_url"),
    path("add_podcast/", AddPodcastView.as_view(),name='add_podcast'),
    path("update/", UpdatePodcastView.as_view(),name='update'),
]