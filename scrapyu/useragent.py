from fake_useragent import UserAgent


class UserAgentMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.ua = UserAgent()
        cls.ua_type = crawler.settings.get('USERAGENT_TYPE', 'random')
        return cls()

    def process_request(self, request, spider):
        ua = getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', ua)