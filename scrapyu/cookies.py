from selenium import webdriver

from .utils import get_firefox_cookies


class FirefoxCookiesMiddleware(object):
    """使用Selenium驱动打开Firefox浏览器获取网页Cookies
    Firefox浏览器版本 69.0.1, geckodriver版本要和浏览器版本对应
    geckodriver下载: https://github.com/mozilla/geckodriver/releases
    Chrome浏览器的headless模式好像出了点问题, 就用Firefox浏览器好了
    """

    def process_request(self, request, spider):
        request.cookies = get_firefox_cookies(request.url)