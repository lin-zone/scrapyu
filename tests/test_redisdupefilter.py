from testfixtures import LogCapture

from scrapy.http import Request
from scrapy.utils.request import request_fingerprint
from scrapy.utils.test import get_crawler

from scrapyu import RedisDupeFilter


def test_redis_filter():
    settings = dict(
        DUPEFILTER_CLASS='scrapyu.RedisDupeFilter',
        REDIS_DUPE_HOST='localhost',
        REDIS_DUPE_PORT=6379,
        REDIS_DUPE_DATABASE=0,
        REDIS_DUPE_PASSWORD=None,
        REDIS_DUPE_KEY='test-scrapyu-requests',
    )
    dupefilter = RedisDupeFilter.from_settings(settings)
    dupefilter.open()
    dupefilter.redis.delete(dupefilter.key)

    r1 = Request('http://scrapytest.org/1')
    r2 = Request('http://scrapytest.org/2')
    r3 = Request('http://scrapytest.org/2')

    assert not dupefilter.request_seen(r1)
    assert dupefilter.request_seen(r1)

    assert not dupefilter.request_seen(r2)
    assert dupefilter.request_seen(r3)

    dupefilter.close('finished')
    

def test_redis_filter_log():
    with LogCapture() as l:
        settings = dict(
            DUPEFILTER_CLASS='scrapyu.RedisDupeFilter',
            REDIS_DUPE_HOST='localhost',
            REDIS_DUPE_PORT=6379,
            REDIS_DUPE_DATABASE=0,
            REDIS_DUPE_PASSWORD=None,
            REDIS_DUPE_KEY='test-scrapyu-requests',
        )
        crawler = get_crawler(settings_dict=settings)
        spider = crawler._create_spider('foo')

        dupefilter = RedisDupeFilter.from_settings(settings)
        dupefilter.open()
        dupefilter.redis.delete(dupefilter.key)

        r1 = Request('http://scrapytest.org/index.html')
        r2 = Request('http://scrapytest.org/index.html',
            headers={'Referer': 'http://scrapytest.org/INDEX.html'}
        )
    
        dupefilter.log(r1, spider)
        dupefilter.log(r2, spider)
    
        assert crawler.stats.get_value('dupefilter/filtered') == 2
        l.check_present(('scrapyu.RedisDupeFilter', 'DEBUG',
            ('Filtered duplicate request: <GET http://scrapytest.org/index.html>'
            ' (referer: None)')))
        l.check_present(('scrapyu.RedisDupeFilter', 'DEBUG',
            ('Filtered duplicate request: <GET http://scrapytest.org/index.html>'
            ' (referer: http://scrapytest.org/INDEX.html)')))
        
        dupefilter.close('finished')
