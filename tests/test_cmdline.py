import subprocess
from tempfile import mkdtemp, TemporaryFile

from path import Path

from tests import TEST_DIR


def test_genspider_list():
    args = "scrapyu genspider -l"
    res = subprocess.check_output(args)
    assert res == b'Available templates:\r\n  single\r\n  single_splash\r\n'


def test_single_template():
    single_test_template = Path(TEST_DIR) / 'test_templates' / 'single.py'
    cwd = mkdtemp()
    args = "scrapyu genspider single www.scrapytest.org -t single"
    with TemporaryFile() as out:
        subprocess.call(args, stdout=out, stderr=out, cwd=cwd)
    t = Path(cwd) / 'single.py'
    assert t.exists() is True
    assert t.read_text() == single_test_template.read_text()


def test_single_splash_template():
    single_splash_test_template = Path(TEST_DIR) / 'test_templates' / 'single_splash.py'
    cwd = mkdtemp()
    args = "scrapyu genspider single-splash www.scrapytest.org -t single_splash"
    with TemporaryFile() as out:
        subprocess.call(args, stdout=out, stderr=out, cwd=cwd)
    t = Path(cwd) / 'single_splash.py'
    assert t.exists() is True
    assert t.read_text() == single_splash_test_template.read_text()