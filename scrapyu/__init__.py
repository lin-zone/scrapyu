__version__ = '0.1.7'


from ._useragent import UserAgentMiddleware
from ._markdown import MarkdownPipeline
from ._cookies import FirefoxCookiesMiddleware
from ._mongodb import MongoDBPipeline
from ._redis import RedisDupeFilter
