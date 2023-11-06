# In the name of GOD

import re

item_tag_pattern = re.compile("<item>((\n|.)*?)</item>")
tag_pattern = re.compile("<([^\<\>\[\]\- ]*)(\s*(\S*)=\"([^\"]*?)\"[^\>\]\[]*)*>")
key_value_pair_pattern = re.compile('([^ ]*?)=\"(.*?)\"')
tag_value_pattern = "(?:<tag.*?>)(.*?)(?:<\/tag>)"
self_close_value_pattern = "(?:<tag[^\<\>\[\]\- ]*)([^\<\>\[\]]*?)(?:/>)"

tag_attr_value = "<(?P<tag>[^\/\<\>\[\]\- ]{1,})(?P<attribute>\s*((\S*)=\"([^\"]*?)\")*?[^\>\]\[]*)*?>(?P<value>[^\<\>]*)"
new_t = "<(?P<tag>[^\/\<\>\[\]\- ]{1,})(?P<attribute>\s*((\S*)=\"([^\"]*?)\")*?[^\>\]\[]*)>(?P<value>[^@]*?)</(?P=tag)>"

# \s+[^\<\>\[\]]*?)\/>

# <(?P<tag>[^\/<>\[\]\s]{1,})(?P<attribute>\s+[^<>\[\]\s-]+=\"[^\"]*\")*>(?P<value>[\d\w\n\s\S]*?)<\/(?P=tag)>|(<(?P<self_tag>[^\/<>\[\]\s-]{1,})(?P<self_attribute>\s+[^<>\[\]\s]+=\"[^\"]*\")*\/>)

tag_attr_value_final = "<(?P<tag>[^\/<>\[\]\s]{3,})(?P<attribute>\s+[^\<\>\[\]]*)?>(?P<value>[\s\S]*?)<\/(?P=tag)>|(<(?P<self_tag>[^\/<>\[\]\s-]{1,})(?P<self_attribute>\s+[^\<\>\[\]]*?)\/>)"