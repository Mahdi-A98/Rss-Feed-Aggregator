from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, exceptions

from account.auth import JWTAuthentication
from .serializers import LikeSerializer, CommentSerializer, PlaylistSerializer
from .models import Playlist

# Create your views here.
class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        like_serializer = LikeSerializer(data = request.data, context={"request": request})
        like_serializer.is_valid(raise_exception=True)
        like = like_serializer.save()
        return Response(data={"message":\
        str(_(f" you liked {like.content_object.title} {like.content_object.__class__.__name__} successfully"))}, status=status.HTTP_201_CREATED)


class CommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        comment_serializer = CommentSerializer(data = request.data, context={"request": request})
        comment_serializer.is_valid(raise_exception=True)
        comment = comment_serializer.save()
        return Response(data={"message": \
        str(_(f" you comment on {comment.content_object.title} {comment.content_object.__class__.__name__} successfully"))}, status=status.HTTP_201_CREATED)

class AddToPlaylistView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        DATA =  request.data.copy()
        DATA['account'] = request.user.id
        playlist_serializer = PlaylistSerializer(data = DATA, partial = True)
        playlist_serializer.is_valid(raise_exception=True)
        playlist_serializer.save()
        data={"message":str(_(f"Playlist created successfully"))}
        data.update(playlist_serializer.data)
        return Response(data=data, status=status.HTTP_201_CREATED)
    
    def put(self, request):
        DATA =  request.data.copy()
        DATA['account'] = request.user.id
        playlist_id = DATA.pop("playlist", 0)
        playlist = Playlist.objects.filter(id=playlist_id)
        if not playlist_id or not playlist:
            raise exceptions.NotFound(str(_("playlist not found")))    
        playlist_serializer = PlaylistSerializer(data = DATA, partial = True ,instance=playlist.first())
        playlist_serializer.is_valid(raise_exception=True)
        playlist_serializer.save()
        data = {"message":str(_(f"Playlist updated successfully"))}
        data.update(playlist_serializer.data)
        return Response(data=data, status=status.HTTP_201_CREATED)
