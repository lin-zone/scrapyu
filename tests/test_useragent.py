import pytest
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.utils.test import get_crawler

from scrapyu import UserAgentMiddleware


@pytest.fixture
def middleware_request(request):
    crawler = get_crawler(Spider, settings_dict=request.param)
    spider = crawler._create_spider('foo')
    mw = UserAgentMiddleware.from_crawler(crawler)
    req = Request('http://www.scrapytest.org/')
    mw.process_request(req, spider)
    yield req


@pytest.mark.parametrize(
    'middleware_request',
    ({'USERAGENT_TYPE': 'firefox'},),
    indirect=True,
)
def test_useragent(middleware_request):
    assert 'User-Agent' in middleware_request.headers
