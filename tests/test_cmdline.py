import sys
import subprocess
from tempfile import mkdtemp, TemporaryFile

from path import Path

from tests import TEST_DIR


args = (sys.executable, '-m', 'scrapyu.cmdline')


def test_genspider_list():
    new_args = args + ('genspider', '-l')
    res = subprocess.check_output(new_args)
    assert res == b'Available templates:\r\n  single\r\n  single_splash\r\n'


def test_single_template():
    single_test_template = Path(TEST_DIR) / 'test_templates' / 'single.py'
    cwd = mkdtemp()
    new_args = args + ('genspider', 'single', 'www.scrapytest.org', '-t', 'single')
    with TemporaryFile() as out:
        subprocess.call(new_args, stdout=out, stderr=out, cwd=cwd)
    t = Path(cwd) / 'single.py'
    assert t.exists() is True
    assert t.read_text() == single_test_template.read_text()


def test_single_splash_template():
    single_splash_test_template = Path(TEST_DIR) / 'test_templates' / 'single_splash.py'
    cwd = mkdtemp()
    new_args = args + ('genspider', 'single-splash', 'www.scrapytest.org', '-t', 'single_splash')
    with TemporaryFile() as out:
        subprocess.call(new_args, stdout=out, stderr=out, cwd=cwd)
    t = Path(cwd) / 'single_splash.py'
    assert t.exists() is True
    assert t.read_text() == single_splash_test_template.read_text()