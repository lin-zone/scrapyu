import os
import sys

from scrapy.cmdline import execute

from .settings import TEMPLATES_DIR


def main():
    argv = sys.argv
    if len(argv) > 1:
        cmdname = argv[1]
        if cmdname == 'genspider':
            argv += ['-s', f'TEMPLATES_DIR={TEMPLATES_DIR}']
    execute(argv=argv)


if __name__ == "__main__":
    main()

