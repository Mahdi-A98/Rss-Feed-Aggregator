# In the name of GOD

from .reg_patterns import item_tag_pattern, key_value_pair_pattern, tag_pattern, tag_value_pattern, self_close_value_pattern, tag_attr_value, tag_attr_value_final
import re
import time

def get_text_or_none(data:dict, key):
    if res:=data.get(key, None):
        return res.get('text')
    return None

def get_all_or_none(data:dict, key):
    if res:=data.get(key, None):
        return res.get('_all_')
    return None

def extract_channel(rss_text):
    channel_text =rss_text[rss_text.find('<channel>')+9: rss_text.rfind("</channel>")]
    return channel_text

def extract_podcast_part(channel_text):
    first_item_open_tag_position = channel_text.find("<item>")
    last_item_close_tag_position = channel_text.rfind('</item>')+7
    rss_excluded_episodes = channel_text[:first_item_open_tag_position] + channel_text[last_item_close_tag_position:]
    return rss_excluded_episodes

def extract_episode_part(channel_text):
    first_item_open_tag_position = channel_text.find("<item>")
    last_item_close_tag_position = channel_text.rfind('</item>')+7
    return channel_text[first_item_open_tag_position:last_item_close_tag_position]


def get_data_dictionary3(text):                     
    match_list = re.finditer(tag_attr_value_final,text,re.MULTILINE)                         
    data = {}
    for item in match_list:
        tag = item.group("tag") or item.group("self_tag")
        tag_name = tag.replace(':', "_")
        attr_text = item.group("attribute") or item.group("self_attribute") or ""
        value = {}
        values_item= item.group("value") or ""
        attrs =  dict(re.findall(key_value_pair_pattern, str(attr_text).lstrip()))
        value['attrs'] = attrs
        value["_all_"] = values_item
        if re.search(tag_attr_value_final, values_item): # makes a list of extracted values
            value.update(get_data_dictionary3(values_item))
        else:
            value["text"] =  values_item
        data[tag_name] = value
    return data


def get_episode_data(rss_text, extract_data_func, count=0):
    item_list = item_tag_pattern.findall(rss_text)
    count = count or len(item_list)
    episode_list = []
    for i, item in enumerate(item_list[:count]):
        episode = extract_data_func(item[0])
        episode_list.append(episode)
    return episode_list
