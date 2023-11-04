# In the name of GOD

from rest_framework.serializers import ModelSerializer
from .models import Podcast, PodcastUrl, Episode, Category, EpisodeAuthor, PodcastAuthor, Owner, Image


class OwnerSerializer(ModelSerializer):
    class Meta:
        model = Owner 
        fields = "__all__"
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category 
        fields = "__all__"
class EpisodeAuthorSerializer(ModelSerializer):
    class Meta:
        model = EpisodeAuthor 
        fields = "__all__"
class PodcastAuthorSerializer(ModelSerializer):
    class Meta:
        model = PodcastAuthor
        fields = "__all__"

class PodcastUrlSerializer(ModelSerializer):
    class Meta:
        model = PodcastUrl
        fields = "__all__"
class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image 
        fields = "__all__"

class PodcastSerializer(ModelSerializer):
    podcast_image = ImageSerializer()
    podcast_author = PodcastAuthorSerializer()
    category = CategorySerializer()
    podcast_url = PodcastUrlSerializer()  
    class Meta:
        model = Podcast
        fields = ["title","language" ,"itunes_type" ,"copy_right","explicit" ,
                    "description","pubDate","last_build_date","link","itunes_subtitle",
                    "itunes_keywords","itunes_image","category","podcast_generator",
                    "podcast_author", "podcast_image","podcast_url",]

class EpisodeSerializer(ModelSerializer):
    episode_podcast = PodcastSerializer()
    class Meta:
        model = Episode 
        fields = "__all__"

class PodcastUrlSerializer(ModelSerializer):
    class Meta:
        model = PodcastUrl
        fields = ['url','title']
