#!/usr/bin/env python3
"""Inserisce <link css/rig-blog-article.css?v=N> negli articoli blog (idempotente).

Uso:
  python scripts/apply-blog-article-css.py blog-a.html blog-b.html   # file singoli
  python scripts/apply-blog-article-css.py --all                      # tutti i blog-*.html (esclude blog.html)
  python scripts/apply-blog-article-css.py --all --dry-run            # solo elenco

Regola: TEST-SKILL/skill-design.md §14. Il link va DOPO blog-rich.css / blog-lead-form.css
(fallback: subito prima di </head>). Se esiste gia' con un v= inferiore, lo incrementa a VERSION.
Preserva i line ending (CRLF/LF) di ogni file.
"""
import glob
import os
import re
import sys

VERSION = 9
LEAD_V = 3  # blog-lead-form.css?v=3 (ott 2026: label .72rem, campi 1rem)
LEAD_RE = re.compile(r'(blog-lead-form\.css\?v=)(\d+)')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK_RE = re.compile(r'<link[^>]*rig-blog-article\.css[^>]*>')
ANCHOR_RE = re.compile(r'(<link[^>]*blog-lead-form\.css[^>]*>|<link[^>]*blog-rich\.css[^>]*>)', re.I)


def process(path, dry):
    with open(path, 'rb') as fh:
        raw = fh.read()
    text = raw.decode('utf-8')
    nl = '\r\n' if '\r\n' in text else '\n'
    tag = '<link rel="stylesheet" href="css/rig-blog-article.css?v=%d">' % VERSION
    if LINK_RE.search(text):
        new = LINK_RE.sub(tag, text, count=1)
        status = 'aggiornato' if new != text else 'gia ok'
    else:
        matches = list(ANCHOR_RE.finditer(text))
        if matches:
            m = matches[-1]  # dopo l'ultimo link ancora, cosi' vince in cascata
            new = text[:m.end()] + nl + tag + text[m.end():]
        elif '</head>' in text:
            new = text.replace('</head>', tag + nl + '</head>', 1)
        else:
            return 'SALTATO (no </head>)'
        status = 'inserito'
    # cache busting: blog-lead-form.css e' stato corretto (label/campi/checkbox) → v=LEAD_V
    new2 = LEAD_RE.sub(lambda m: m.group(1) + str(LEAD_V), new)
    if new2 != new:
        new = new2
        status += '+lead-form v=%d' % LEAD_V
    if new != text and not dry:
        with open(path, 'wb') as fh:
            fh.write(new.encode('utf-8'))
    return status


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv
    if '--all' in sys.argv:
        args = [p for p in sorted(glob.glob(os.path.join(ROOT, 'blog-*.html')))]
    if not args:
        print(__doc__)
        return 1
    counts = {}
    for p in args:
        p = p if os.path.isabs(p) else os.path.join(ROOT, p)
        st = process(p, dry)
        counts[st] = counts.get(st, 0) + 1
        if '--all' not in sys.argv or st.startswith('SALTATO'):
            print('%-12s %s' % (st, os.path.basename(p)))
    print(counts)
    return 0


if __name__ == '__main__':
    sys.exit(main())
