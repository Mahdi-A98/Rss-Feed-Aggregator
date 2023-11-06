# In the name of GOD

from .utils import get_text_or_none, get_all_or_none
from abc import ABC, abstractmethod


class ConverterFactory:

    def __init__(self):
        self._converters = {}

    def register_format(self, format, creator):
        self._converters[format] = creator

    def get_converter(self, format, data):
        conveter = self._converters.get(format)
        if not conveter:
            raise ValueError(format)
        return conveter(data)

class Converter(ABC):

    def __init__(self, data):
        self.data = data


    @abstractmethod
    def get_attribute(self):
        pass

    @abstractmethod
    def get_node(self):
        pass


class DictConverter(Converter):
    def __init__(self, data:dict):
        self.data = data

    def _get_attribute(self, attr, data:dict):
        return get_text_or_none(data, attr) or self.get_from_node_attrs(attr) or get_all_or_none(data, attr)

    def get_attribute(self, attr):
        return self._get_attribute(attr, data=self.data)

    def get_node(self, node_name):
        return self.__class__(self.data.get(node_name, {}))

    def get_from_node_attrs(self, key):
        node_attrs = self.data.get("attrs", {})
        return node_attrs.get(key)

    def __bool__(self):
        return bool(self.data)


class ObjectConverter:
    def __init__(self, factory:ConverterFactory):
        self.factory = factory  
    
    def convert(self, format, model, data):
        converter = self.factory.get_converter(format, data)
        model_object = model.convert(converter)
        return model_object

    def convert_to_model(self, format, model, data, instance=None):
        converter = self.factory.get_converter(format, data)
        model_instanse = model.convert(converter, save=False, instance=instance)
        return model_instanse


xml_converter_factory = ConverterFactory()
xml_converter_factory.register_format('dict', DictConverter)

xml_object_converter = ObjectConverter(xml_converter_factory)