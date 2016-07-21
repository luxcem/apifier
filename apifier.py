import requests
import json

from lxml import etree
from cssselect import GenericTranslator
# from collections import namedtuple, OrderedDict

class Apifier:

    def __init__(self,
                 config=None,
                 description_file=None):

        if description_file:
            with open(description_file) as fo:
                config = json.load(fo)
        self.name = config["name"]
        self.url = config["url"]
        self.foreach = config.get("foreach", None)
        self.encoding = config.get("encoding", None)
        self.description = config["description"]
        self.context = config.get("context", None)

    @property
    def items(self):
        return self.description.items()

    @classmethod
    def consolidate(cls, description_list):
        # Concat results from all Apifier
        return [sublist for description_file in description_list for sublist in Apifier(description_file).load()]

    def load_foreach(self):
        # Scrap data over multiple pages
        page = requests.get(self.url)
        tree = etree.HTML(page.text)

        selector = GenericTranslator().css_to_xpath(self.foreach)
        l = [e for e in tree.xpath(selector)]

        # Concat results from all pages
        return [sublist for e in l for sublist in self.load_data(e.get("href"), e.text)]

    def load_data(self, url, context=None):
        page = requests.get(url)
        tree = etree.HTML(page.text)

        if self.encoding:
            l = {key: [e.text.encode(self.encoding).decode("utf-8") for e in tree.xpath(GenericTranslator().css_to_xpath(selector))] for key, selector in self.items}
        else:
            l = {key: [e.text for e in tree.xpath(GenericTranslator().css_to_xpath(selector))] for key, selector in self.items}

        if context:
            # Add a context attribute to the record
            result_len = len(next(iter(l.values())))
            l[self.context] = [context] * result_len

        keys = list(l.keys())
        values = zip(*(l.values()))
        return [dict(zip(keys, t)) for t in values]

    def load(self):
        if self.foreach:
            return self.load_foreach()
        else:
            return self.load_data(self.url)
