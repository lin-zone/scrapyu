import re
from urllib.parse import urlparse

from selenium import webdriver


def get_base_url(url):
    result = urlparse(url)
    base_url = '{}://{}'.format(result.scheme, result.netloc)
    return base_url


def get_domain(url):
    result = urlparse(url)
    return result.netloc


_cookies = dict()


def _get_firefox_cookies(url, **kwargs):
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options, **kwargs)
    browser.set_page_load_timeout(60)
    browser.get(url)
    cookies = browser.get_cookies()
    browser.quit()
    return cookies


def _raw_cookies_to_scrapy_cookies(cookies):
    return {c['name']: c['value'] for c in cookies}


def get_firefox_cookies(url, convert_scrapy_cookies=True, **kwargs):
    base_url = get_base_url(url)
    key = (base_url, convert_scrapy_cookies)
    if key not in _cookies:
        cookies = _get_firefox_cookies(base_url, **kwargs)
        if convert_scrapy_cookies:
            cookies = _raw_cookies_to_scrapy_cookies(cookies)
        _cookies[key] = cookies
    return _cookies[key]


def re_match(pattern, string):
    if not isinstance(pattern, str):
        return False
    bound = r'\b'
    if not pattern.startswith(bound):
        pattern = bound + pattern
    if not pattern.endswith(bound):
        pattern += bound
    compile_pattern = re.compile(pattern)
    return bool(compile_pattern.match(string))