import os
from tempfile import TemporaryDirectory

import html2text
from scrapy.spiders import Spider
from scrapy.utils.test import get_crawler

from scrapyu import MarkdownPipeline


with open('normal.html') as f:
    html = f.read()

with open('normal.md') as f:
    text = f.read()
    

def test_html2text():
    h = html2text.HTML2Text()
    h.ignore_links = True
    assert text == h.handle(html)


def test_markdown_pipeline():
    item = {}
    item['html'] = html
    item['filename'] = filename = 'normal'
    tempdir = TemporaryDirectory().name
    tempfile = os.path.join(tempdir, filename) + '.md'
    crawler = get_crawler(Spider, settings_dict=dict(MARKDOWNS_STORE=tempdir))
    spider = crawler._create_spider('foo')
    pipe = MarkdownPipeline()
    pipe.open_spider(spider)
    pipe.process_item(item, spider)
    with open(tempfile) as f:
        result = f.read()
    assert text == result
