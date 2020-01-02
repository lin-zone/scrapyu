import os
from tempfile import TemporaryDirectory

import html2text
from path import Path
from scrapy.spiders import Spider
from scrapy.utils.test import get_crawler

from scrapyu import MarkdownPipeline


base_path = os.path.realpath(os.path.dirname(__file__))
html = (Path(base_path) / 'normal.html').read_text()
text = (Path(base_path) / 'normal.md').read_text()
    

def test_html2text():
    h = html2text.HTML2Text()
    h.ignore_links = True
    assert text == h.handle(html)


def test_markdown_pipeline():
    item = {}
    item['html'] = html
    item['filename'] = filename = 'normal'
    tempdir = TemporaryDirectory().name
    crawler = get_crawler(Spider, settings_dict=dict(MARKDOWNS_STORE=tempdir))
    spider = crawler._create_spider('foo')
    pipe = MarkdownPipeline()
    pipe.open_spider(spider)
    pipe.process_item(item, spider)
    result = (Path(tempdir) / '{}.md'.format(filename)).read_text()
    assert text == result
