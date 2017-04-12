import json
import urllib
from copy import deepcopy

import requests
from lxml import etree
from cssselect import GenericTranslator


class Apifier:

    _config_error = ValueError("Incorrect configuration, check the docs")
    _config_allowed_keys = ("name", "url", "foreach", "next", "encoding",
                            "description", "context", "prefix", "xpath")

    def __init__(self, config):
        # Avoid side effect on config
        config = deepcopy(config)

        if isinstance(config, str):
            with open(config) as fo:
                config = json.load(fo)

        self._check_config(config)

        self.name = config.get("name", None)
        self.url = config["url"]
        self.xpath = config.get("xpath", False)
        self.prefix = config.get("prefix", "")
        self.foreach = self._get_selector(config.get("foreach", None))
        self.next = self._get_selector(config.get("next", None))
        self.encoding = config.get("encoding", None)
        self.description = config["description"]
        self.context = config.get("context", None)

    def _get_selector(self, selector):
        if not selector:
            return selector

        if self.xpath:
            return selector
        else:
            return GenericTranslator().css_to_xpath(selector)

    def _check_config(self, config):
        if not isinstance(config, dict):
            raise self._config_error

        if "url" not in config or "description" not in config:
            raise self._config_error

        if not config["url"] or not config["description"]:
            raise self._config_error

        for key in config:
            if key not in self._config_allowed_keys:
                raise self._config_error

    @property
    def items(self):
        return self.description.items()

    def _load_foreach(self):
        """Scrap data over multiple pages"""
        page = requests.get(self.url)
        tree = etree.HTML(page.text)

        results = []
        for elem in tree.xpath(self.foreach):
            next_url = urllib.parse.urljoin(self.url, elem.get("href"))
            results.extend(self._load_data(next_url, elem.text))
        return results

    def _load_next(self):
        """Scrap data over multiple pages with a next link"""
        page = requests.get(self.url)
        tree = etree.HTML(page.text)

        results = []

        i = 1
        results.extend(self._load_data(self.url, i))
        while tree.xpath(self.next):
            i += 1
            e = tree.xpath(self.next)[0]
            next_url = urllib.parse.urljoin(self.url, e.get("href"))
            results.extend(self._load_data(next_url,  i))
            next_page = requests.get(next_url)
            tree = etree.HTML(next_page.text)
        return results

    def _get_text_content(self, node):
        """Iter over text inside the node
        Element.itertext() removes tags"""
        text = "".join(node.itertext())
        if self.encoding:
            text = text.encode(self.encoding).decode("utf-8")
        return text.strip()

    def _load_data(self, url, context=None):
        page = requests.get(url)
        tree = etree.HTML(page.text)
        l = {}
        # Transform the css selector to xpath if asked
        for key, selector in self.items:
            selector = self._get_selector("{}{}".format(
                self.prefix,
                selector
            ))
            l[key] = []
            for e in tree.xpath(selector):
                # If e is a lxml instance of element get e.text
                if isinstance(e, etree._Element):
                    l[key].append(self._get_text_content(e))
                else:
                    l[key].append(e)

        if context:
            # Add a context attribute to the record
            result_len = len(next(iter(l.values())))
            l[self.context] = [context] * result_len

        keys = list(l.keys())
        values = zip(*(l.values()))
        return [dict(zip(keys, t)) for t in values]

    def load(self):
        if self.foreach:
            return self._load_foreach()
        elif self.next:
            return self._load_next()
        else:
            return self._load_data(self.url)
