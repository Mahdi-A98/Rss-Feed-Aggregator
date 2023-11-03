# In the name of GOD

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from account.auth import JWTAuthentication
from .models import Podcast, Episode
from .serializer import PodcastSerializer, PodcastUrlSerializer
from .utils import Parser
from feedback.serializer import LikeSerializer, CommentSerializer, PlaylistSerializer
from feedback.models import Like, Comment, Playlist

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



class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        print(request.user)
        like_serializer = LikeSerializer(data = request.data, context={"request": request})
        like_serializer.is_valid(raise_exception=True)
        like_serializer.save()
        return Response(data={"message":str(_("success"))}.update(like_serializer.data), status=status.HTTP_201_CREATED)


class CommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        print(request.user)
        comment_serializer = CommentSerializer(data = request.data)
        comment_serializer.is_valid(raise_exception=True)
        if comment_serializer.validated_data.get('model')=="podcast":
            podcast = Podcast.objects.get(id = comment_serializer.validated_data.get("model_id"))
            if podcast:
                comment = Comment(content_object = podcast, account = request.user, text = comment_serializer.validated_data.get("text"))
                comment.save()
        elif comment_serializer.validated_data.get('model') == "episode":
            episode = Episode.objects.get(id = comment_serializer.validated_data.get("model_id"))
            if episode:
                comment = Comment(content_object = episode, account = request.user, text = comment_serializer.validated_data.get("text"))
                comment.save()
        return Response(data={"message":str(_("success"))}, status=status.HTTP_201_CREATED)


class PlaylistView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        DATA =  request.data.copy()
        DATA['account'] = request.user
        DATA.pop("playlist")
        playlist_serializer = PlaylistSerializer(data = DATA, partial = True ,instance=Playlist.objects.get(id=request.data.get("playlist")))
        playlist_serializer.is_valid(raise_exception=True)
        playlist_serializer.save()
        return Response(data={"message":str(_("success"))}, status=status.HTTP_201_CREATED)
