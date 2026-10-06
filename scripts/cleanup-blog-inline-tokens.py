#!/usr/bin/env python3
"""Pulizia inline blog: --grigio vecchio, font troppo piccoli (§14). Idempotente."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'blog.html', 'blog-articolo.html', 'blog-prova-mercato-limena-zona-imma-2027.html'}


def main():
    n = 0
    for path in glob.glob(os.path.join(ROOT, 'blog-*.html')):
        if os.path.basename(path) in SKIP:
            continue
        text = open(path, encoding='utf-8', errors='replace').read()
        orig = text
        text = re.sub(r'--grigio:\s*#6B7A8D', '--grigio:#556578', text, flags=re.I)
        text = re.sub(r'--grigio:\s*#6b7a8d', '--grigio:#556578', text)
        text = re.sub(r'font-size:\s*\.58rem', 'font-size:.7rem', text)
        text = re.sub(r'font-size:\s*\.5[0-9]rem', 'font-size:.7rem', text)
        text = re.sub(r'font-size:\s*\.62rem', 'font-size:.72rem', text)
        text = re.sub(r'font-weight:\s*300(?=[^0-9])', 'font-weight:700', text)
        if text != orig:
            try:
                open(path, 'wb').write(text.encode('utf-8'))
                n += 1
            except OSError as e:
                print('skip', os.path.basename(path), e)
    print('updated', n)


if __name__ == '__main__':
    main()
