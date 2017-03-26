# Apifier

Apifier is a very simple HTML parser written in Python.

It aims to parse HTML document in a declarative way using css selectors. Its
main purpose is to parse tabular and/or paginated data.

## Install

Apifier is available for python 3

[![Build Status](https://travis-ci.org/luxcem/apifier.svg?branch=master)](https://travis-ci.org/luxcem/apifier)
[![codecov](https://codecov.io/gh/luxcem/vizhash/branch/master/graph/badge.svg)](https://codecov.io/gh/luxcem/vizhash)

```
pip install apifier
```

## Example

Getting all comments from
[an article](http://www.lefigaro.fr/politique/le-scan/2016/07/21/25001-20160721ARTFIG00062-attentat-de-nice-la-droite-demande-une-enquete-independante.php)
at "LeFigaro.fr"

```
from apifier import Apifier

config = {
    "name": "FigaroBot article comments",
    "encoding": "latin-1",
    "url": "http://www.lefigaro.fr/politique/le-scan/2016/07/21/25001-20160721ARTFIG00062-attentat-de-nice-la-droite-demande-une-enquete-independante.php",
    "foreach": "#fig-pagination-nav > li > a",
    "context": "page",
    "raw_selectors": [],
    "prefix": ""#reagir > div > div > div.fig-col.fig-col--comments > div:nth-child(3) > ul > li > article >",
    "description": {
        "author": "div.fig-comment-header a",
        "comment": "div.fig-comment-msg p"
    }
}

api = Apifier(config=config)
data = api.load()
```

## Config

+ name : name of the current configuration
+ encoding : is the encoding the page is using, data will be converted from this encoding to utf-8 for sanity
+ url : page url, first page in case of paginated data
+ foreach : css selector for the pagination links int this example pagination looks like :
  ```
  <ul id="fig-pagination-nav">
    <li class="fig-pagination-current"><a href="…"> 1 </a></li>
    <li><a href="…"> 2 </a></li>
    <li><a href="…"> 3 </a></li>
  </ul>
  ```
+ context : each data will be associated with a special variable named after the content of the pagination link
  in this case, this content is just the page number, but the pagination mechanism can be used for othher purpose
  like categories
+ raw_selectors : list of fields in description which are raw xpath selectors instead of css selectors (for example if you want to get element attributes)  
+ prefix : descriptors will be prefixed by this option
+ description : descriptor for content to parse, in this example, comment content and author name.

The result looks like this :

```
    data =
    [
        {'comment': "…", 'author': '…', 'page': '1'}, etc
    ]
```
