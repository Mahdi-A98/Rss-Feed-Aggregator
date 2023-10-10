from django.db import models
class Like(BaseModel):
    account = models.ForeignKey(User,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.account

class Comment(BaseModel):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.account.phone
class Playlist(BaseModel):
    title = models.CharField(max_length=40)
    description = models.TextField(blank=False,null=True)
    account = models.ForeignKey(User,on_delete=models.CASCADE)

    podcasts = models.ManyToManyField(Podcast)
    episodes = models.ManyToManyField(Episode)


    def __str__(self) -> str:
        return self.title
