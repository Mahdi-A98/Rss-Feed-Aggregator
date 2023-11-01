from django.contrib import admin
from .models import Podcast, Owner, Category, Image, Episode, Generator, PodcastUrl, EpisodeAuthor, PodcastAuthor #, Author, Enclosure
# Register your models here.


admin.site.register(Podcast)
admin.site.register(Owner)
# admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Episode)
# admin.site.register(Enclosure)
admin.site.register(Generator)
admin.site.register(PodcastUrl)
admin.site.register(EpisodeAuthor)
admin.site.register(PodcastAuthor)