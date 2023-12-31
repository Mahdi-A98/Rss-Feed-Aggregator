from django.contrib import admin
from .models import Podcast, Owner, Category, Image, Episode, Generator, PodcastUrl, EpisodeAuthor, PodcastAuthor #, Author, Enclosure
# Register your models here.


admin.site.register(Podcast)
admin.site.register(Owner)
# admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Image)
# admin.site.register(Episode)
# admin.site.register(Enclosure)
admin.site.register(Generator)
# admin.site.register(PodcastUrl)
admin.site.register(EpisodeAuthor)
admin.site.register(PodcastAuthor)

@admin.register(Episode) 
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ["id", "title","pubDate","episode_author","episode_podcast"]
    search_fields = ["title", "description", "id"]
    list_filter = ['pubDate', 'episode_podcast']


@admin.register(PodcastUrl) 
class PodcastUrlAdmin(admin.ModelAdmin):
    list_display = ["id", "title","url","is_saved",]
    search_fields = ["title", "url", "id"]
    list_editable = ['is_saved']