# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest


class SingleSplashSpider(scrapy.Spider):
    name = 'single-splash'
    allowed_domains = ['www.scrapytest.org/']

    def start_reqeusts(self):
        yield SplashRequest('http://www.scrapytest.org/')

    def parse(self, response):
        pass


DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
SPLASH_URL='http://192.168.99.100:8050/',

settings = dict(
    DOWNLOADER_MIDDLEWARES=DOWNLOADER_MIDDLEWARES,
    SPIDER_MIDDLEWARES=SPIDER_MIDDLEWARES,
    DUPEFILTER_CLASS=DUPEFILTER_CLASS,
    HTTPCACHE_STORAGE=HTTPCACHE_STORAGE,
    SPLASH_URL=SPLASH_URL,
)


def main():
    process = CrawlerProcess(settings)
    process.crawl(SingleSplashSpider)
    process.start()


if __name__ == "__main__":
    main()