# scrapyu

[![Build Status](https://www.travis-ci.org/lin-zone/scrapyu.svg?branch=master)](https://www.travis-ci.org/lin-zone/scrapyu)
[![codecov](https://codecov.io/gh/lin-zone/scrapyu/branch/master/graph/badge.svg)](https://codecov.io/gh/lin-zone/scrapyu)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scrapyu?logo=python&logoColor=FBE072)](https://pypi.org/project/scrapyu/)
[![GitHub](https://img.shields.io/github/license/lin-zone/scrapyu)](https://github.com/lin-zone/scrapyu/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lin-zone/scrapyu?logo=github)](https://github.com/lin-zone/scrapyu)
[![GitHub forks](https://img.shields.io/github/forks/lin-zone/scrapyu?logo=github)](https://github.com/lin-zone/scrapyu)

## `UserAgentMiddleware`

```python
# settings.py
USERAGENT_TYPE = 'firefox'
```

## `MarkdownPipeline`

```python
# settings.py
MARKDOWNS_STORE = 'news'
```

```python
# items.py
import scrapy

class MdItem(scrapy.Item):
    html = scrapy.Field()
    filename = scrapy.Field()
```
