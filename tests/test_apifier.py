import os
import pytest

from copy import deepcopy
from httmock import HTTMock, all_requests
from apifier import Apifier


@all_requests
def mock_wikipedia(url, request):
    path = os.path.dirname(os.path.realpath(__file__)) + "/data/python.html"
    with open(path, "r") as fo:
        return fo.read()


@all_requests
def mock_next(url, request):
    path = (os.path.dirname(os.path.realpath(__file__)) +
            "/data" + url.path)
    with open(path, "r") as fo:
        return fo.read()


_python_versions = [{"date": "13 avril 1999", "version": "1.5(.2)"},
                    {"date": "5 septembre 2000", "version": "1.6"},
                    {"date": "16 octobre 2000", "version": "2.0"},
                    {"date": "17 avril 2001", "version": "2.1"},
                    {"date": "21 décembre 2001", "version": "2.2"},
                    {"date": "29 juillet 2003", "version": "2.3"},
                    {"date": "30 novembre 2004", "version": "2.4"},
                    {"date": "19 septembre 2006", "version": "2.5"},
                    {"date": "1er octobre 2008", "version": "2.6"},
                    {"date": "3 juillet 2010", "version": "2.7"},
                    {"date": "3 décembre 2008", "version": "3.0"},
                    {"date": "27 juin 2009", "version": "3.1"},
                    {"date": "20 février 2011", "version": "3.2"},
                    {"date": "29 septembre 2012", "version": "3.3"},
                    {"date": "16 mars 2014", "version": "3.4"},
                    {"date": "13 septembre 2015", "version": "3.5"}]

_simple_config = {
    "name": "Test",
    "url": "http://en.wikipedia.org/python",
    "prefix": ("#mw-content-text > "
               "table.wikitable.sortable > tbody > tr >"),
    "description": {
        "version": "td:nth-child(1)",
        "date": "td:nth-child(2) time",
    }
}

_simple_config_xpath = deepcopy(_simple_config)
_simple_config_xpath["xpath"] = True
_simple_config_xpath["prefix"] = '//*[@id="mw-content-text"]/table[3]/' \
                                 "tbody/tr/"
_simple_config_xpath["description"]["version"] = "td[1]"
_simple_config_xpath["description"]["date"] = "td[2]/time"

_simple_config_foreach = {
    "name": "Test",
    "url": "http://en.wikipedia.org/python",
    "encoding": "utf-8",
    "xpath": True,
    "context": "year",
    "foreach": '//*[@id="mw-content-text"]/table[3]/tbody/tr/td[2]/time/a[3]',
    "description": {
        "title": "//h1/text()",
    }
}

_simple_config_next = {
    "name": "Test",
    "url": "http://text_next.org/test_next1.html",
    "xpath": True,
    "context": "page",
    "next": '/html/body/a[@class="next"]',
    "description": {
        "name": "/html/body/ul/li",
    }
}


def test_init():
    assert isinstance(Apifier(_simple_config), Apifier)


def test_simple():
    with HTTMock(mock_wikipedia):
        api = Apifier(_simple_config)
        data = api.load()
        assert len(data) == 16
        assert data == _python_versions


def test_config_json():
    config_path = os.path.dirname(
        os.path.realpath(__file__)) + "/data/conf.json"
    with HTTMock(mock_wikipedia):
        api = Apifier(config_path)
        data = api.load()
        assert len(data) == 16
        assert data == _python_versions


def test_xpath():
    with HTTMock(mock_wikipedia):
        api = Apifier(_simple_config_xpath)
        data = api.load()
        assert len(data) == 16
        assert data == _python_versions


def test_fail():
    with pytest.raises(ValueError):
        Apifier(None)
    with pytest.raises(ValueError):
        fail_conf = deepcopy(_simple_config)
        fail_conf["url"] = None
        Apifier(fail_conf)
    with pytest.raises(ValueError):
        fail_conf = deepcopy(_simple_config)
        fail_conf["description"] = None
        Apifier(fail_conf)
    with pytest.raises(ValueError):
        fail_conf = deepcopy(_simple_config)
        del fail_conf["url"]
        Apifier(fail_conf)
    with pytest.raises(ValueError):
        fail_conf = deepcopy(_simple_config)
        del fail_conf["description"]
        Apifier(fail_conf)
    with pytest.raises(ValueError):
        fail_conf = deepcopy(_simple_config)
        fail_conf["wrong_key"] = True
        Apifier(fail_conf)


def test_foreach():
    with HTTMock(mock_wikipedia):
        api = Apifier(_simple_config_foreach)
        data = api.load()
        assert len(data) == 16
        years = ["1999", "2000", "2000", "2001", "2001", "2003", "2004",
                 "2006", "2008", "2010", "2008", "2009", "2011", "2012",
                 "2014", "2015"]
        for i, elem in enumerate(data):
            assert elem["year"] == years[i]
            assert elem["title"] == "Python (langage)"


def test_next():
    with HTTMock(mock_next):
        api = Apifier(_simple_config_next)
        data = api.load()
        i = 1
        for result in data:
            assert result["name"] == "Test {}".format(i)
            i += 1
