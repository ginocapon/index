#!/usr/bin/env python3
"""Controlli statici rapidi (no browser) post-allineamento blog §14."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
issues = {}


def main():
    for path in sorted(glob.glob(os.path.join(ROOT, 'blog-*.html'))):
        name = os.path.basename(path).replace('.html', '')
        if name == 'blog':
            continue
        t = open(path, encoding='utf-8', errors='replace').read()
        bad = []
        if 'rig-blog-article.css?v=' not in t:
            bad.append('manca rig-blog-article.css')
        if re.search(r'--grigio:#6B7A8D', t, re.I):
            bad.append(':root --grigio vecchio')
        if re.search(r'font-size:\s*\.5[0-9]rem', t):
            bad.append('font < .6rem inline')
        if bad:
            issues[name] = bad
    print('file con problemi statici:', len(issues))
    for k, v in list(issues.items())[:15]:
        print(k, v)
    return 0 if not issues else 1


if __name__ == '__main__':
    raise SystemExit(main())
