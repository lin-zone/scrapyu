# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess


class SingleSpider(scrapy.Spider):
    name = 'single'
    allowed_domains = ['www.scrapytest.org']
    start_urls = ['http://www.scrapytest.org/']

    def parse(self, response):
        pass


#ITEM_PIPELINES = {
#    'crawler.pipelines.CrawlerPipeline': 300,
#}
#SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerSpiderMiddleware': 543,
#}
#DOWNLOADER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerDownloaderMiddleware': 543,
#}

settings = dict(
#    ITEM_PIPELINES=ITEM_PIPELINES,
#    SPIDER_MIDDLEWARES=SPIDER_MIDDLEWARES,
#    DOWNLOADER_MIDDLEWARES=DOWNLOADER_MIDDLEWARES,
)


def main():
    process = CrawlerProcess(settings)
    process.crawl(SingleSpider)
    process.start()


if __name__ == "__main__":
    main()