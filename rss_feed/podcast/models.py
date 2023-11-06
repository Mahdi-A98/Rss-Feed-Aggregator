# In the name of GOD

from django.db import models
from core.models import BaseModel
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class PodcastAuthor(BaseModel):
    name = models.CharField(max_length=30)

    @classmethod
    def convert(cls, converter, save=True, *args, **kwargs):
        if not converter.get_attribute('itunes_author'):
            return None
        if not save:
            podcast_author  = cls(name=converter.get_attribute('itunes_author'))
            return podcast_author
        podcast_author, created = cls.objects.get_or_create(name=converter.get_attribute('itunes_author'))
        return podcast_author

    def __str__(self):
        return self.name


class EpisodeAuthor(models.Model):
    name = models.CharField(max_length=30, unique=True)

    @classmethod
    def convert(cls, converter, save=True, *args, **kwargs):
        if not converter.get_attribute('itunes_author'):
            return None
        if not save:
            episode_author  = cls(name=converter.get_attribute('itunes_author'))
            return episode_author
        episode_author, created = cls.objects.get_or_create(name=converter.get_attribute('itunes_author'))
        return episode_author

    def __str__(self):
        return f'{self.name}'

class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    @classmethod
    def convert(cls, converter, save=True, *args, **kwargs):
        category_name = converter.get_attribute('text') or converter.get_node('itunes_category').get_from_node_attrs('text')
        if not category_name:
            return None
        if not save:
            category  = cls(name=category_name)
            return category
        category, created = cls.objects.get_or_create(name=category_name)
        return category

    def __str__(self):
        return self.name


class Owner(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    @classmethod
    def convert(cls, converter, save=True, *args, **kwargs):
        owner_node = converter.get_node('itunes_owner')
        if not owner_node:
            return None
        if not save:
            model_object = cls(name=owner_node.get_attribute('itunes_name'),
                                email=owner_node.get_attribute('itunes_email'))
            return model_object    
        model_object, created = cls.objects.get_or_create(name=owner_node.get_attribute('itunes_name'),
                                                    email=owner_node.get_attribute('itunes_email'))
        return model_object

    def __str__(self):
        return self.name


class Image(BaseModel):
    url = models.URLField(unique=True, max_length=400)

    title = models.CharField(max_length=100,null=True,blank=True)
    @classmethod
    def convert(cls, converter, save=True, *args, **kwargs):
        image_node = converter.get_node('image') or converter.get_node('itunes_image')
        image_url = image_node.get_attribute('url') or image_node.get_attribute('href')
        if not image_url:
            return None
        if not save:
            image = cls(url=image_url,title= image_node.get_attribute('title'), link=image_node.get_attribute('link'))
            return image

        image, created = cls.objects.get_or_create(url=image_url,
                                        title=image_node.get_attribute('title'),
                                        link=image_node.get_attribute('link'))
        return image

    def __str__(self):
        return f'{self.url}'


class Generator(BaseModel):
    name = models.CharField(max_length=100)

    hostname = models.CharField(max_length=150,null=True,blank=True)
    genDate = models.DateTimeField(null=True,blank=True)

    @classmethod
    def convert(cls, converter, save=True, *args, **kwargs):
        if not converter.get_attribute('generator'):
            return None
        if not save:
            generator = cls(name=converter.get_attribute('generator'))
            return generator
        generator, created = cls.objects.get_or_create(name=converter.get_attribute('generator'))
        return generator
    def __str__(self):
        return self.name


class PodcastUrl(BaseModel):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=150)
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        return self.url

class Podcast(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    itunes_type = models.CharField(max_length=50)
    copy_right = models.CharField(max_length=100)
    explicit = models.CharField(max_length=50)
    description = models.TextField() #We use description for itunes summary too.
    pubDate = models.DateTimeField(null=True,blank=True)
    last_build_date = models.DateTimeField(null=True,blank=True)
    link = models.URLField(null=True,blank=True)
    itunes_subtitle = models.TextField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)
    itunes_image = models.CharField(max_length=400)
    category = models.ManyToManyField(Category)
    podcast_generator = models.ForeignKey(Generator,on_delete=models.CASCADE,null=True)
    podcast_author = models.ForeignKey(PodcastAuthor,on_delete=models.CASCADE)
    podcast_image = models.OneToOneField(Image,on_delete=models.CASCADE)
    podcast_url = models.OneToOneField(PodcastUrl, on_delete=models.PROTECT)

    @classmethod
    def convert(cls, converter, save=True, instance=None, *args, **kwargs):
        deffered_data = {}
        for key in cls.__dict__.keys():
            if type(cls.__dict__[key]).__name__ == "DeferredAttribute":
                deffered_data[key] = converter.get_attribute(key)
        deffered_data["copy_right"] = converter.get_attribute("copyright")  
        deffered_data["pubDate"] = datetime.strptime(converter.get_attribute("pubDate"), "%a, %d %b %Y %H:%M:%S %z") if converter.get_attribute("pubDate") else None
        deffered_data["lastBuildDate"] = datetime.strptime(converter.get_attribute("lastBuildDate"), "%a, %d %b %Y %H:%M:%S %z") if converter.get_attribute("lastBuildDate") else None
        if instance:
            deffered_data.pop("id")
            for item, value in deffered_data.items():
                setattr(instance, item, value)
            return instance
        if not save:
            podcast = cls(**deffered_data)
            return podcast
        podcast, created = cls.objects.get_or_create(**deffered_data)
        return podcast
    def __str__(self):
        return f"{self.id}: {self.title}"

class Episode(models.Model):
    title = models.CharField(max_length=100) #We use title for itunes_title too.
    guid = models.CharField(max_length=150)
    itunes_duration = models.CharField(max_length=50)
    itunes_episode_type = models.CharField(max_length=50)
    itunes_explicit = models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField() #We use description for itunes summary and content_encoded too.
    enclosure = models.CharField(null=True, blank=True,max_length=300)
    link = models.URLField(null=True,blank=True)
    pubDate = models.DateTimeField(null=True,blank=True)
    itunes_keywords = models.TextField(null=True, blank=True)
    itunes_player = models.CharField(null=True, blank=True,max_length=100) #We use itunes_player for fireside_playerEmbedCode too.
    episode_podcast = models.ForeignKey(Podcast,on_delete=models.CASCADE, related_name="episode")
    episode_author = models.ForeignKey(EpisodeAuthor,on_delete=models.CASCADE,null=True)

    @classmethod
    def convert(cls, converter, save=True, *args, **kwargs):
        deffered_data = {}
        for key in cls.__dict__.keys():
            if type(cls.__dict__[key]).__name__ == "DeferredAttribute":
                deffered_data[key] = converter.get_attribute(key)
        deffered_data["pubDate"] = datetime.strptime(converter.get_attribute("pubDate"), "%a, %d %b %Y %H:%M:%S %z") if converter.get_attribute("pubDate") else None
        if not save:    
            episode = cls(**deffered_data)
            return episode
        episode, created = cls.objects.get_or_create(**deffered_data)
        return episode
    def __str__(self):
        return f"{self.id}: {self.title}"

#******************************************* NEW MODELS ***************************************************
# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True,)
#     parent_category = models.ForeignKey('self', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

# class Author(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=100, null=True, blank=True, unique=True)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey("content_type", "object_id")



#     def __str__(self):
#         return f"{self.id}: {self.name}"


# class Owner(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField(null=True, blank=True, unique=True)

#     def __str__(self):
#         return f"{self.id}: {self.name}"

# class Image(models.Model):
#     title = models.CharField(max_length=100, null=True, blank=True)
#     link = models.URLField(null=True, blank=True)
#     url = models.URLField()

#     def __str__(self):
#         return f"{self.id}: {self.title}"

# class Generator(models.Model):
#     name = models.CharField(max_length=100)
#     hostname = models.CharField(max_length=150, null=True, blank=True)
#     genDate = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.id}: {self.name}"


# class Enclosure(models.Model):
#     url = models.URLField()
#     length = models.PositiveIntegerField(null=True, blank=True)
#     c_type = models.CharField(max_length=30, null=True, blank=True)


# class Podcast(BaseModel):
#     """
#         required tags are title, description, image, language, category and explicit
#     """
#     title = models.CharField(max_length=100)
#     description = models.TextField() #We use description for itunes summary too.
#     image = models.OneToOneField(Image,on_delete=models.PROTECT)
#     language = models.CharField(max_length=50)
#     category = models.ManyToManyField(Category)
#     explicit = models.CharField(max_length=50)
#     itunes_type = models.CharField(max_length=50, null=True, blank=True)
#     copy_right = models.CharField(max_length=100, null=True, blank=True)
#     pubDate = models.DateTimeField(null=True,blank=True)
#     last_build_date = models.DateTimeField(null=True,blank=True)
#     link = models.URLField(null=True,blank=True)
#     itunes_subtitle = models.TextField(null=True,blank=True)
#     itunes_keywords = models.TextField(null=True, blank=True)
#     generator = models.ForeignKey(Generator,on_delete=models.CASCADE, null=True, blank=True)
#     author = GenericRelation(Author)
#     # (Author,on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"{self.id}: {self.title}"


# class Episode(models.Model):
#     """
#         required tags are title, enclosure
#     """
#     episode_podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100) #We use title for itunes_title too.
#     enclosure = models.ForeignKey(Enclosure, on_delete=models.CASCADE)
#     guid = models.CharField(max_length=400, null=True, blank=True)
#     itunes_duration = models.CharField(max_length=50, null=True, blank=True)
#     itunes_episode_type = models.CharField(max_length=50, null=True, blank=True)
#     itunes_explicit = models.CharField(max_length=50, null=True, blank=True)
#     description = models.TextField(null=True, blank=True) #We use description for itunes summary and content_encoded too.
#     link = models.URLField(null=True,blank=True)
#     pub_date = models.DateTimeField(null=True,blank=True)
#     itunes_keywords = models.TextField(null=True, blank=True)
#     itunes_player = models.CharField(max_length=50, null=True, blank=True) #We use itunes_player for fireside_playerEmbedCode too.
#     author = GenericRelation(Author)
#     # author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f"{self.id}: {self.title}"
