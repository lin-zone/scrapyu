import logging

from redis import Redis
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import referer_str, request_fingerprint

from .utils import re_match


class RedisDupeFilter(BaseDupeFilter):

    def __init__(self, host, port, db, password, key, ignore_url):
        self.redis = Redis(host, port, db, password)
        self.key = key
        self.ignore_url = ignore_url
        self.fingerprints = self.redis.smembers(key)
        self.logger = logging.getLogger('scrapyu.RedisDupeFilter')

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_DUPE_HOST', 'localhost')
        port = settings.get('REDIS_DUPE_PORT', 6379)
        db = settings.get('REDIS_DUPE_DATABASE', 0)
        password = settings.get('REDIS_DUPE_PASSWORD')
        key = settings.get('REDIS_DUPE_KEY', 'requests')
        ignore_url = settings.get('REDIS_DUPE_IGNORE_URL')
        return cls(host, port, db, password, key, ignore_url)

    def request_seen(self, request):
        if re_match(self.ignore_url, request.url):
            return False
        fp = request_fingerprint(request)
        fp = bytes(fp, encoding='utf-8')
        if fp in self.fingerprints:
            return True
        else:
            self.fingerprints.add(fp)
            return False

    def close(self, reason):
        if self.fingerprints:
            self.redis.sadd(self.key, *self.fingerprints)
        self.redis.close()

    def log(self, request, spider):
        msg = "Filtered duplicate request: %(request)s (referer: %(referer)s)"
        args = {'request': request, 'referer': referer_str(request) }
        self.logger.debug(msg, args, extra={'spider': spider})
        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
