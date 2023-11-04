# In the name of GOD

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from account.auth import JWTAuthentication
from .models import Podcast, Episode
from .serializer import PodcastSerializer, PodcastUrlSerializer
from .utils import Parser

from .tasks import save_podcast
from django.utils.translation import gettext_lazy as _


class PodcastListView(APIView):
    def get(self, request):
        query = Podcast.objects.all()
        serializer = PodcastSerializer(instance=query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EpisodeListView(APIView):
    def get(self, request):
        queryset = Episode.objects.all()
        serializer_data = EpisodeSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)


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
