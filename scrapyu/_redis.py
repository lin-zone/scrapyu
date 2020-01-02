import logging

from redis import Redis
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import referer_str, request_fingerprint


class RedisDupeFilter(BaseDupeFilter):

    def __init__(self, host, port, db, password, key):
        self.redis = Redis(host, port, db, password)
        self.key = key
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_DUPE_HOST', 'localhost')
        port = settings.get('REDIS_DUPE_PORT', 6379)
        db = settings.get('REDIS_DUPE_DATABASE', 0)
        password = settings.get('REDIS_DUPE_PASSWORD')
        key = settings.get('REDIS_DUPE_KEY', 'requests')
        return cls(host, port, db, password, key)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if self.redis.sismember(self.key, fp):
            return True
        self.redis.sadd(self.key, fp)

    def close(self, reason):
        self.redis.close()

    def log(self, request, spider):
        msg = "Filtered duplicate request: %(request)s (referer: %(referer)s)"
        args = {'request': request, 'referer': referer_str(request) }
        self.logger.debug(msg, args, extra={'spider': spider})
        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
