# In the name of GOD

from django.db import models
from core.models import BaseModel
# from author.models import PodcastAuthor, EpisodeAuthor
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True,)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True, unique=True)


    def __str__(self):
        return f"{self.id}: {self.name}"


class Owner(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.id}: {self.name}"

class Image(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return f"{self.id}: {self.title}"

class Generator(models.Model):
    name = models.CharField(max_length=100)
    hostname = models.CharField(max_length=150, null=True, blank=True)
    genDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Enclosure(models.Model):
    url = models.URLField()
    length = models.PositiveIntegerField(null=True, blank=True)
    c_type = models.CharField(max_length=30, null=True, blank=True)


class Podcast(BaseModel):
    """
        required tags are title, description, image, language, category and explicit
    """
    title = models.CharField(max_length=100)
    description = models.TextField() #We use description for itunes summary too.
    image = models.OneToOneField(Image,on_delete=models.PROTECT)
    language = models.CharField(max_length=50)
    category = models.ManyToManyField(Category)
    explicit = models.CharField(max_length=50)
    itunes_type = models.CharField(max_length=50, null=True, blank=True)
    copy_right = models.CharField(max_length=100, null=True, blank=True)
    pubDate = models.DateTimeField(null=True,blank=True)
    last_build_date = models.DateTimeField(null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    itunes_subtitle = models.TextField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)
    generator = models.ForeignKey(Generator,on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(Author,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Episode(models.Model):
    """
        required tags are title, enclosure
    """
    episode_podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) #We use title for itunes_title too.
    enclosure = models.ForeignKey(Enclosure, on_delete=models.CASCADE)
    guid = models.CharField(max_length=400, null=True, blank=True)
    itunes_duration = models.CharField(max_length=50, null=True, blank=True)
    itunes_episode_type = models.CharField(max_length=50, null=True, blank=True)
    itunes_explicit = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True) #We use description for itunes summary and content_encoded too.
    link = models.URLField(null=True,blank=True)
    pub_date = models.DateTimeField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)
    itunes_player = models.CharField(max_length=50, null=True, blank=True) #We use itunes_player for fireside_playerEmbedCode too.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title}"
