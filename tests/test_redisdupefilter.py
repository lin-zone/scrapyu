from testfixtures import LogCapture

from scrapy.http import Request
from scrapy.utils.request import request_fingerprint
from scrapy.utils.test import get_crawler

from scrapyu import RedisDupeFilter


def clear_redis_set(dupe):
    dupe.redis.delete(dupe.key)


def test_redis_filter():
    settings = dict(
        DUPEFILTER_CLASS='scrapyu.RedisDupeFilter',
        REDIS_DUPE_HOST='localhost',
        REDIS_DUPE_PORT=6379,
        REDIS_DUPE_DATABASE=0,
        REDIS_DUPE_PASSWORD=None,
        REDIS_DUPE_KEY='test-scrapyu-requests',
    )
    dupe = RedisDupeFilter.from_settings(settings)
    clear_redis_set(dupe)
    dupe.open()

    r1 = Request('http://scrapytest.org/1')
    r2 = Request('http://scrapytest.org/2')
    r3 = Request('http://scrapytest.org/2')

    assert not dupe.request_seen(r1)
    assert dupe.request_seen(r1)

    assert not dupe.request_seen(r2)
    assert dupe.request_seen(r3)

    dupe.close('finished')
    clear_redis_set(dupe)
    

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

        dupe = RedisDupeFilter.from_settings(settings)
        dupe.open()
        clear_redis_set(dupe)

        r1 = Request('http://scrapytest.org/index.html')
        r2 = Request('http://scrapytest.org/index.html',
            headers={'Referer': 'http://scrapytest.org/INDEX.html'}
        )
    
        dupe.log(r1, spider)
        dupe.log(r2, spider)
    
        assert crawler.stats.get_value('dupefilter/filtered') == 2
        l.check_present(('scrapyu.RedisDupeFilter', 'DEBUG',
            ('Filtered duplicate request: <GET http://scrapytest.org/index.html>'
            ' (referer: None)')))
        l.check_present(('scrapyu.RedisDupeFilter', 'DEBUG',
            ('Filtered duplicate request: <GET http://scrapytest.org/index.html>'
            ' (referer: http://scrapytest.org/INDEX.html)')))
        
        dupe.close('finished')
        clear_redis_set(dupe)


def test_ignore_url():
    settings = dict(
        DUPEFILTER_CLASS='scrapyu.RedisDupeFilter',
        REDIS_DUPE_HOST='localhost',
        REDIS_DUPE_PORT=6379,
        REDIS_DUPE_DATABASE=0,
        REDIS_DUPE_PASSWORD=None,
        REDIS_DUPE_KEY='test-scrapyu-requests',
        REDIS_DUPE_IGNORE_URL=r'http://scrapytest.org/\d+'
    )
    dupe = RedisDupeFilter.from_settings(settings)
    dupe.open()

    r1 = Request('http://scrapytest.org/1')
    r2 = Request('http://scrapytest.org/23')
    r3 = Request('http://scrapytest.org/a')
    r4 = Request('http://scrapytest.org/1a')

    assert not dupe.request_seen(r1)
    assert not dupe.request_seen(r1)

    assert not dupe.request_seen(r2)
    assert not dupe.request_seen(r2)

    assert not dupe.request_seen(r3)
    assert dupe.request_seen(r3)  
  
    assert not dupe.request_seen(r4)
    assert dupe.request_seen(r4)

    dupe.close('finished')
    clear_redis_set(dupe)

def test_restart():
    settings = dict(
        DUPEFILTER_CLASS='scrapyu.RedisDupeFilter',
        REDIS_DUPE_HOST='localhost',
        REDIS_DUPE_PORT=6379,
        REDIS_DUPE_DATABASE=0,
        REDIS_DUPE_PASSWORD=None,
        REDIS_DUPE_KEY='test-scrapyu-requests',
    )
    dupe = RedisDupeFilter.from_settings(settings)
    dupe.open()

    r1 = Request('http://scrapytest.org/1')
    r2 = Request('http://scrapytest.org/2')
    r3 = Request('http://scrapytest.org/2')
    r4 = Request('http://scrapytest.org/3')

    dupe.request_seen(r1)
    dupe.request_seen(r2)
    dupe.request_seen(r3)
    dupe.close('finished')

    dupe = RedisDupeFilter.from_settings(settings)
    dupe.open()
    assert len(dupe.fingerprints) == 2

    assert dupe.request_seen(r1)
    assert dupe.request_seen(r2)
    assert dupe.request_seen(r3)
    assert not dupe.request_seen(r4)

    assert len(dupe.fingerprints) == 3

    dupe.close('finished')
    clear_redis_set(dupe)
    