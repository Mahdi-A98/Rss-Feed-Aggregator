# In the name of GOD 
from django.urls import path
from . import views

app_name="podcast"
urlpatterns = [
    path("podcasts/", views.PodcastListView.as_view(), name="podcasts"),
    path('episodes/<int:podcast_id>/', views.EpisodeListView.as_view(), name='episode'),
    path("add_podcast_url/", views.AddPodcastUrlView.as_view(), name="add_podcast_url"),
    path("add_podcast/", views.AddPodcastView.as_view(),name='add_podcast'),
    path("update/", views.UpdatePodcastView.as_view(),name='update'),
    path("recommendation/", views.RecommendationView.as_view(),name='recommendation'),
]