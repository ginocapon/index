#!/usr/bin/env python3
"""Aggiorna link author-bio blog → pagine autore E-E-A-T."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    ('href="chi-siamo">Scopri il team &rarr;', 'href="gino-capon">Profilo autore &rarr;'),
    ('href="chi-siamo">Scopri il team →', 'href="gino-capon">Profilo autore →'),
    ('href="chi-siamo">Chi siamo</a>', 'href="gino-capon">Profilo autore</a>'),
    ('href="chi-siamo">Chi Siamo</a>', 'href="gino-capon">Profilo autore</a>'),
]

AUTHOR_LINK = '<p style="font-size:.78rem;margin-top:.4rem"><a href="gino-capon">Profilo autore</a></p>'


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if 'author-bio' not in text:
        return False
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if 'Linda Righetto' in text or 'Righetto Linda' in text:
        text = text.replace('href="gino-capon"', 'href="linda-righetto"')
    if 'author-bio' in text and 'href="gino-capon"' not in text and 'href="linda-righetto"' not in text:
        if 'Gino Capon' in text:
            marker = '</div>\n  </div>\n\n<!-- ARTICOLI CORRELATI -->'
            if marker in text and AUTHOR_LINK not in text:
                text = text.replace(
                    '</div>\n  </div>\n\n<!-- ARTICOLI CORRELATI -->',
                    AUTHOR_LINK + '\n  </div>\n\n<!-- ARTICOLI CORRELATI -->',
                    1,
                )
            elif '</div></div>' in text and AUTHOR_LINK not in text:
                idx = text.find('author-bio')
                if idx >= 0:
                    end = text.find('</div>', text.find('</div>', idx) + 1)
                    if end >= 0 and AUTHOR_LINK not in text[idx:end + 20]:
                        text = text[: end + 6] + AUTHOR_LINK + text[end + 6 :]
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    changed = 0
    for path in sorted(ROOT.glob('blog-*.html')):
        if patch_file(path):
            changed += 1
            print('updated', path.name)
    print(f'Done: {changed} file aggiornati')


if __name__ == '__main__':
    main()
