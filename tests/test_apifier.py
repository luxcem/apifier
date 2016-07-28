import os

from httmock import urlmatch, HTTMock
from apifier import Apifier


@urlmatch(netloc=r'(.*\.)?wikipedia\.org(/(.*))?$')
def mock_wikipedia(url, request):
    path = os.path.dirname(os.path.realpath(__file__)) + '/data/python.html'
    with open(path, 'r') as fo:
        return fo.read()

_python_versions = [{'date': '13 avril 1999', 'version': '1.5(.2)'},
                    {'date': '5 septembre 2000', 'version': '1.6'},
                    {'date': '16 octobre 2000', 'version': '2.0'},
                    {'date': '17 avril 2001', 'version': '2.1'},
                    {'date': '21 décembre 2001', 'version': '2.2'},
                    {'date': '29 juillet 2003', 'version': '2.3'},
                    {'date': '30 novembre 2004', 'version': '2.4'},
                    {'date': '19 septembre 2006', 'version': '2.5'},
                    {'date': '1er octobre 2008', 'version': '2.6'},
                    {'date': '3 juillet 2010', 'version': '2.7'},
                    {'date': '3 décembre 2008', 'version': '3.0'},
                    {'date': '27 juin 2009', 'version': '3.1'},
                    {'date': '20 février 2011', 'version': '3.2'},
                    {'date': '29 septembre 2012', 'version': '3.3'},
                    {'date': '16 mars 2014', 'version': '3.4'},
                    {'date': '13 septembre 2015', 'version': '3.5'}]

_simple_config = {
    'name': 'Test',
    'url': 'http://en.wikipedia.org/python',
    'prefix': ('#mw-content-text > '
               'table.wikitable.sortable > tbody > tr >'),
    'description': {
        'version': 'td:nth-child(1)',
        'date': 'td:nth-child(2) time',
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
