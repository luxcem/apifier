from distutils.core import setup
__version__ = '1.1.0'
setup(
    name='apifier',
    packages=['apifier'],
    version=__version__,
    description='A web parser for tabular and/or paginated data',
    author='luxcem',
    author_email='a@luxcem.fr',
    url='https://github.com/luxcem/apifier',
    download_url='https://github.com/luxcem/apifier/tarball/{}'.format(
        __version__),
    keywords=['api', 'parser', 'table data', 'html parser'],
    classifiers=[],
    install_requires=[
        'requests',
        'cssselect',
        'lxml'
    ],
    tests_require=[
        'httmock'
    ]
)
