# In the name of GOD

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from account.auth import JWTAuthentication
from .models import Podcast, Episode
from feedback.models import Playlist
from .serializer import PodcastSerializer, PodcastUrlSerializer, EpisodeSerializer
from .utils import Parser

from .tasks import save_podcast, update_podcast
from django.utils.translation import gettext_lazy as _


class PodcastListView(generics.ListAPIView):
    serializer_class = PodcastSerializer
    queryset = Podcast.objects.all()


class EpisodeListView(generics.ListAPIView):
    serializer_class = EpisodeSerializer
    # queryset = Episode.objects.all()

    def get_queryset(self):
        podcast = Podcast.objects.filter(id=self.kwargs.get('podcast_id', 0))
        if podcast:
            episode_list = Episode.objects.filter(episode_podcast=podcast.first()).prefetch_related("episode_podcast")
        return episode_list
        



class AddPodcastUrlView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def post(self,request):
        serializer = PodcastUrlSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message': str(_("URL is saved"))}, status=status.HTTP_201_CREATED)

class AddPodcastView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAdminUser]

    def post(self, request):
        data = request.data['url']
        if not data:
            raise Response({'message':str(_('URL is invalid!'))}, status=status.HTTP_400_BAD_REQUEST)
        save_podcast.delay(data)
        return Response({"message":str(_("Rss file save in database successfully."))}, status.HTTP_201_CREATED)



class UpdatePodcastView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data['xml']
        if not data:
            raise Response({'message':str(_('xml is invalid!'))}, status=status.HTTP_400_BAD_REQUEST)
        update_podcast.delay(data)
        return Response({"message":str(_("xml is going to update"))}, status.HTTP_201_CREATED)

class RecommendationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request):
        categories = Playlist.objects.filter(account=request.user).values_list("podcasts__category__name")
        categories = list(map(lambda item:item[0], categories))
        recommended_podcast = Podcast.objects.filter(category__name__in=categories)[:10]
        serializer = PodcastSerializer(instance=recommended_podcast, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)