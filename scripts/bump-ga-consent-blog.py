#!/usr/bin/env python3
"""Allinea js/ga-consent.js?v=13 negli articoli blog (carica atmosphere v17 + disclosure v8)."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = 13
RE = re.compile(r'(js/ga-consent\.js\?v=)\d+')


def main():
    n = 0
    for path in glob.glob(os.path.join(ROOT, 'blog-*.html')):
        text = open(path, encoding='utf-8', errors='replace').read()
        new = RE.sub(r'\g<1>' + str(TARGET), text)
        if new != text:
            nl = '\r\n' if '\r\n' in text else '\n'
            open(path, 'wb').write(new.encode('utf-8'))
            n += 1
    print('updated', n)


if __name__ == '__main__':
    main()
