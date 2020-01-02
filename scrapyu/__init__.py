__version__ = '0.1.6'


from .useragent import UserAgentMiddleware
from .markdown import MarkdownPipeline
from .cookies import FirefoxCookiesMiddleware
from .mongodb import MongoDBPipeline
