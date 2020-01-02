__version__ = '0.1.7'


from .useragent import UserAgentMiddleware
from .markdown import MarkdownPipeline
from .cookies import FirefoxCookiesMiddleware
from .mongodb import MongoDBPipeline
from ._redis import RedisDupeFilter
