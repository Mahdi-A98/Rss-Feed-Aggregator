# In the name of GOD

import requests
from abc import ABC, abstractmethod
from podcast.models import Category, Owner, Image, Generator, PodcastUrl
from .converters import xml_object_converter
from .utils import extract_channel, extract_episode_part, extract_podcast_part
from .utils import get_data_dictionary3, get_episode_data

class Xml:
    def __init__(self):
        self.podcast_fk_models = {}
        self.episode_fk_models = {}
        self.episode_mtm_models = {}
        self.episode_mtm_models = {}


class BaseParser:
    def __init__(self, *args, **kwargs):
        self.xml_object_converter = xml_object_converter
        self.url = kwargs.get('podcast_url')
        self.rss_path = kwargs.get('rss_path')
        self.rss_file = kwargs.get('rss_file')
        self.xml = kwargs.get('xml_model')
        self.podcast_dict ={}
        self.episodes_obj = []


    def _read_rss_file(self):
        with open(self.rss_path, "rt", encoding="utf-8") as file:
            rss_file = file.read()
        return rss_file

    def get_episode_data(self):
        channel_text = extract_channel(self.rss_file)
        epiodes_text = extract_episode_part(channel_text)
        episode_dicts = get_episode_data(epiodes_text, get_data_dictionary3)
        self.episode_dicts = episode_dicts
        return episode_dicts

    def get_podcast_data(self):
        channel_text = extract_channel(self.rss_file)
        podcast_text = extract_podcast_part(channel_text)
        podcast_dict = get_data_dictionary3(podcast_text)
        self.podcast_dict = podcast_dict
        return podcast_dict
