# In the name of GOD
import re
import datetime as dt
from django.db.models import Max
import logging

from .models import Podcast, Episode, Owner, Category, Generator, Image, PodcastAuthor, EpisodeAuthor
from .xml_parser.parser import BaseParser, Xml
from .xml_parser.converters import DictConverter
# from main.publisher import Publish

# logger = logging.getLogger("django-celery")

XmlBaseModel = Xml()
XmlBaseModel.podcast_fk_models.update({"podcast_owner": Owner, "podcast_generator":Generator, "podcast_author": PodcastAuthor, "podcast_image": Image})
XmlBaseModel.podcast_mtm_models = {"category": Category,}
XmlBaseModel.episode_fk_models.update({"episode_author":EpisodeAuthor,})

class Parser(BaseParser):

    def __init__(self, rss_path=None, rss_file=None, save=False, podcast_url=None, *args, **kwargs):
        super().__init__(rss_path=None, rss_file=None, save=False, podcast_url=None, *args, **kwargs)
        self.rss_path = rss_path
        self.rss_file = rss_file or self._read_rss_file()
        self.podcast_data = DictConverter(self.podcast_dict or self.get_podcast_data())
        podcast_object = Podcast.objects.filter(title=self.podcast_data.get_attribute("title"), link= self.podcast_data.get_attribute("link"))
        self.podcast_object = podcast_object.first() if podcast_object else None
        self.url = podcast_url or self.podcast_object.podcast_url
        self.episodes_obj = list()
        self.xml_model = XmlBaseModel
        if save:
            self.save_podcast_in_db() if not self.check_exist()[0] else None
            self.save_episode() if not self.check_exist()[1] else None


    def check_exist(self):
        podcast_data = self.podcast_data
        old_podcast = Podcast.objects.filter(title=podcast_data.get_attribute('title'), link=podcast_data.get_attribute('link'))
        if old_podcast:
            if old_podcast.first().episode.all():
                return True,True
            return True,False
        return False,False

    
    def update_podcast_fields(self):
        return self.save_or_update_podcast_in_db(instance=self.podcast_object)


    def save_podcast_in_db(self):
        #--save podcast--#
        assert self.check_exist()[0] == False, "Podcast already exist."
        return self.save_or_update_podcast_in_db()

    def save_episode(self):
        assert self.check_exist()[1] == False, "Episodes already exist."
        episodes = self.get_episode_data()
        author_list = self.get_author_objects(episodes)

        self.save_episode_in_db(episodes, author_list, self.podcast_object)



    def save_episode_in_db(self,episode_list,author_list,podcast_object):
        res_list = []
        for index, episode in enumerate(episode_list):
            episode_model = self.xml_object_converter.convert_to_model(format='dict', model=Episode, data=episode)
            episode_model.episode_author = author_list[index]
            episode_model.episode_podcast = podcast_object
            res_list.append(episode_model)
        Episode.objects.bulk_create(res_list)
        self.episodes_obj = res_list
        return res_list 


    def update_exist_podcast(self):
        episodes = self.get_episode_data()
        podcast_object = self.podcast_object
        if not podcast_object:
            return "This podcast didn't save in database"
        podcast_object = self.update_podcast_fields()    # Important
        episode_objects_list = Episode.objects.filter(episode_podcast=podcast_object).values_list("guid",flat=True)
        if self.podcast_data.get_attribute("pubDate"):
            podcast_last_update = dt.datetime.strptime(self.podcast_data.get_attribute("pubDate"),"%a, %d %b %Y %H:%M:%S %z")  
        else:
            podcast_last_update = max(list(map(lambda item:dt.datetime.strptime(item.get("pubDate").get("text"),"%a, %d %b %Y %H:%M:%S %z"), episodes)))

        podcast_object_last_update = podcast_object.pubDate or Episode.objects.aggregate(Max("pubDate")).get("pubDate__max")
        episode_update_list = []
        if podcast_object_last_update < podcast_last_update or len(episodes)>len(episode_objects_list):
            for new_episode in episodes:
                if DictConverter(new_episode).get_attribute("guid") not in episode_objects_list:
                    episode_update_list.append(new_episode)
            author_list = self.get_author_objects(episode_update_list)

            self.save_episode_in_db(episode_update_list, author_list, podcast_object)
            # Publish().update_podcast(podcast=podcast_object)
            print(f"{podcast_object.title} Updated successfully")
            return f"{podcast_object.title} Updated successfully"

        return "xml file has not new episode for update!!" + podcast_object.title   



    def set_fk_models(self, fk_dict, instance, model_class, data):
        for model_name, model in fk_dict.items():
            assert type(model_class.__dict__[model_name]).__name__ not in ["ManyToManyDescriptor", "ReverseManyToOneDescriptor"]
            obj = self.xml_object_converter.convert(format='dict', model=model, data=data)
            if obj:
                setattr(instance, model_name, obj)
        return instance


    def set_mtm_models(self, mtm_dict, instance, model_class, data):
        for model_name, model in mtm_dict.items():
            assert type(model_class.__dict__[model_name]).__name__ == "ManyToManyDescriptor", f"relation of {model_name} to {model_class} is not many to many"
            obj = self.xml_object_converter.convert(format='dict', model=model, data=data)
            if obj:
                obj.save()
                getattr(instance, model_name).add(obj)
        return instance


    def get_author_objects(self, episode_list):
        author_list = []
        unique_authors = {}

        for episode in episode_list:
            author = unique_authors.get(DictConverter(episode).get_attribute('itunes_author')) or self.xml_object_converter.convert(format='dict', model=EpisodeAuthor, data=episode)
            unique_authors[getattr(author, 'name', None)] = author
            author_list.append(author)
        unique_authors.pop(None, None)
        return author_list


    def save_or_update_podcast_in_db(self, instance=None):
        instance = instance or self.podcast_object
        podcast_data = self.podcast_dict or self.get_podcast_data()
        podcast_model = self.xml_object_converter.convert_to_model(format='dict', model=Podcast, data=podcast_data, instance=instance)
        podcast_model.podcast_url = self.url
        podcast_model = self.set_fk_models(self.xml_model.podcast_fk_models, podcast_model, Podcast, podcast_data)
        podcast_model.save()
        podcast_model = self.set_mtm_models(self.xml_model.podcast_mtm_models, podcast_model, Podcast, podcast_data)
        podcast_model.save()
        podcast_model.podcast_url.is_save = True
        podcast_model.podcast_url.save()
        self.podcast_object = podcast_model
        return podcast_model