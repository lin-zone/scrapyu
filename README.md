# scrapyu

[![Build Status](https://www.travis-ci.org/lin-zone/scrapyu.svg?branch=master)](https://www.travis-ci.org/lin-zone/scrapyu)
[![codecov](https://codecov.io/gh/lin-zone/scrapyu/branch/master/graph/badge.svg)](https://codecov.io/gh/lin-zone/scrapyu)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scrapyu?logo=python&logoColor=FBE072)](https://pypi.org/project/scrapyu/)
[![GitHub](https://img.shields.io/github/license/lin-zone/scrapyu)](https://github.com/lin-zone/scrapyu/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lin-zone/scrapyu?logo=github)](https://github.com/lin-zone/scrapyu)
[![GitHub forks](https://img.shields.io/github/forks/lin-zone/scrapyu?logo=github)](https://github.com/lin-zone/scrapyu)

## UserAgentMiddleware

```python
# settings.py
USERAGENT_TYPE = 'firefox'
DOWNLOADER_MIDDLEWARES = {
   'scrapyu.UserAgentMiddleware': 543,
}
```

## MarkdownPipeline

```python
# settings.py
MARKDOWNS_STORE = 'news'
ITEM_PIPELINES = {
    'scrapyu.MarkdownPipeline': 300,
}
```

```python
# items.py
import scrapy

class MarkdownItem(scrapy.Item):
    html = scrapy.Field()
    filename = scrapy.Field()
```

## FirefoxCookiesMiddleware

```python
# settings.py
GECKODRIVER_PATH = 'geckodriver'
DOWNLOADER_MIDDLEWARES = {
   'scrapyu.FirefoxCookiesMiddleware': 543,
}
```

## MongoDBPipeline

```python
# settings.py
MONGODB_URI = 'mongodb://localhost:27017'
# or
# MONGODB_HOST = 'localhost'
# MONGODB_PORT = 27017
MONGODB_DATABASE = 'scrapyu'
MONGODB_COLLECTION = 'items'
MONGODB_UNIQUE_KEY = 'title name'
# or
# MONGODB_UNIQUE_KEY = ['title', 'name']
# MONGODB_UNIQUE_KEY = ('title', 'name')
ITEM_PIPELINES = {
    'scrapyu.MongoDBPipeline': 300,
}
```

## RedisDupeFilter

```python
# settings.py
DUPEFILTER_CLASS = 'scrapyu.RedisDupeFilter'
REDIS_DUPE_HOST = 'localhost'
REDIS_DUPE_PORT = 6379
REDIS_DUPE_DATABASE = 0
REDIS_DUPE_PASSWORD = 'password'
REDIS_DUPE_KEY = 'requests'
```
