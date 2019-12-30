import pytest


from scrapyu.utils import get_base_url, get_domain


url = "https://github.com/lin-zone/scrapyu"


def test_get_base_url():
    assert "https://github.com" == get_base_url(url)


def test_get_domain():
    assert "github.com" == get_domain(url)
