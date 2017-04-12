from distutils.core import setup
__version__ = '2.1.0'

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
    keywords='api parser table data html',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: XML",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    install_requires=[
        'requests',
        'cssselect',
        'lxml'
    ],
    tests_require=[
        'httmock',
        'pytest',
        'pytest-cov'
    ]
)
