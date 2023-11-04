# In the name of GOD

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from core.models import BaseModel
from account.models import User
from podcast.models import Podcast, Episode


class Like(BaseModel):
    account = models.ForeignKey(User,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.account.username} liked {self.content_object.title} {self.content_object.__class__.__name__}"

class Comment(BaseModel):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.account.username} commented on  {self.content_object.title} {self.content_object.__class__.__name__}"


class Playlist(BaseModel):
    title = models.CharField(max_length=40)
    description = models.TextField(blank=False,null=True)
    account = models.ForeignKey(User,on_delete=models.CASCADE)

    podcasts = models.ManyToManyField(Podcast)
    episodes = models.ManyToManyField(Episode)

    class Meta:
        unique_together = ('account', 'title')

    def __str__(self) -> str:
        return f"{self.title} playlist for {self.account.username} "
