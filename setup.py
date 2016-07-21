from distutils.core import setup
setup(
    name = 'apifier',
    packages = ['apifier'],
    version = '1.0.3',
    description = 'A web parser for tabular and/or paginated data',
    author = 'luxcem',
    author_email = 'a@luxcem.fr',
    url = 'https://github.com/luxcem/apifier',
    download_url = 'https://github.com/luxcem/apifier/tarball/1.0.3',
    keywords = ['api', 'parser', 'table data', 'html parser'],
    classifiers = [],
    install_requires=[
        "requests",
        "cssselect",
        "lxml"
    ],
)
