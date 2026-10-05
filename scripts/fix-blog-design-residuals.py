#!/usr/bin/env python3
"""Fix residui design blog (date visibili, h3 sintesi, font inline). Vedi skill-design §14."""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE_VIS = re.compile(r'(Ultimo aggiornamento|Aggiornamento|Aggiornato)[^\n]{0,60}20\d\d', re.I)
DATE_MOD = re.compile(r'"dateModified"\s*:\s*"([^"]+)"', re.I)
DATE_PUB = re.compile(r'"datePublished"\s*:\s*"([^"]+)"', re.I)

SKIP = {'blog.html', 'blog-articolo.html', 'blog-prova-mercato-limena-zona-imma-2027.html'}


def nl(text):
    return '\r\n' if '\r\n' in text else '\n'


def fix_file(path):
    with open(path, 'rb') as fh:
        raw = fh.read()
    text = raw.decode('utf-8')
    if os.path.basename(path) in SKIP:
        return 'skip'
    changed = False
    n = nl(text)

    if not DATE_VIS.search(text):
        dm = DATE_MOD.search(text) or DATE_PUB.search(text)
        if dm:
            d = dm.group(1)[:10]
            parts = d.split('-')
            months = 'gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre'.split()
            label = '%s %s %s' % (int(parts[2]), months[int(parts[1]) - 1], parts[0]) if len(parts) == 3 else d
            block = '<p class="art-update-line" style="font-size:.8rem;color:var(--grigio,#556578);margin-top:1.5rem"><strong>Aggiornamento:</strong> %s.</p>' % label
            if '</article>' in text:
                text = text.replace('</article>', block + n + '</article>', 1)
                changed = True
            elif '<footer' in text:
                text = text.replace('<footer', block + n + '<footer', 1)
                changed = True

    new, n1 = re.subn(r'<h3>In sintesi([^<]*)</h3>', r'<h2 class="aeo-kicker">In sintesi\1</h2>', text, flags=re.I)
    if n1:
        text, changed = new, True
    if '.aeo-kicker' not in text and 'aeo-kicker' in text:
        ins = '.aeo-kicker{font-family:\'Montserrat\',sans-serif;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--blu);margin:0 0 .55rem}'
        if '</style>' in text:
            text = text.replace('</style>', ins + n + '</style>', 1)
            changed = True

    new, n2 = re.subn(r'\.art-content th\{background:var\(--sfondo\)', '.art-content th{background:var(--blu);color:var(--bianco)', text)
    if n2:
        text, changed = new, True

    new, n3 = re.subn(r'font-size:\s*\.68rem', 'font-size:.72rem', text)
    if n3:
        text, changed = new, True

    new, n4 = re.subn(r'\.art-content p\{([^}]*?)font-size:\s*\.88rem', r'.art-content p{\1font-size:1rem', text)
    if n4:
        text, changed = new, True

    orig = raw.decode('utf-8')
    if changed and text != orig:
        try:
            with open(path, 'wb') as fh:
                fh.write(text.encode('utf-8'))
            return 'ok'
        except OSError as e:
            return 'err:' + str(e)[:40]
    return '—'


def main():
    stats = {}
    for path in sorted(glob.glob(os.path.join(ROOT, 'blog-*.html'))):
        st = fix_file(path)
        stats[st] = stats.get(st, 0) + 1
    print(stats)


if __name__ == '__main__':
    main()
