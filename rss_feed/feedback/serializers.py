# In the name of GOD

from rest_framework import serializers
from .models import Playlist, Like, Comment
from podcast.models import Podcast, Episode



class LikeSerializer(serializers.Serializer):
    model = serializers.CharField(max_length = 50)
    model_id = serializers.IntegerField()

    def create(self, validated_data):
        request = self.context['request']
        if validated_data["model"] == "podcast":
            podcast = Podcast.objects.get(id=validated_data["model_id"])
            if podcast:
                like = Like(content_object = podcast, account = request.user)
                like.save()
        elif validated_data["model"] == "episode":
            episode = Episode.objects.get(id=validated_data["model_id"])
            if episode:
                like = Like(content_object = episode, account = request.user)
                like.save()
        return like


class CommentSerializer(serializers.Serializer):
    model = serializers.CharField(max_length = 50)
    model_id = serializers.IntegerField()
    text = serializers.CharField()

    def create(self, validated_data):
        request = self.context['request']
        if validated_data["model"] == "podcast":
            podcast = Podcast.objects.get(id=validated_data["model_id"])
            if podcast:
                comment = Comment(content_object = podcast, account = request.user, text=validated_data['text'])
                comment.save()
        elif validated_data["model"] == "episode":
            episode = Episode.objects.get(id=validated_data["model_id"])
            if episode:
                comment = Comment(content_object = episode, account = request.user, text=validated_data['text'])
                comment.save()
        return comment


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['title','description','account','podcasts','episodes']

    def update(self, instance, validated_data):
        for podcast in validated_data.get("podcasts", []):
            instance.podcasts.add(podcast)
        for episode in validated_data.get("episodes", []):
            instance.episodes.add(episode)
        instance.save()
        return instance

