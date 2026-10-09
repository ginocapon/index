"""Inserisce/aggiorna il blocco movimento "stile iOS" (<style id="rig-motion">) in tutte le pagine pubbliche.

Transizione tra pagine (View Transitions cross-document), scroll fluido sulle ancore e comparse
più lente con la curva di iOS. Solo CSS, disattivato con prefers-reduced-motion.
Rieseguibile: sostituisce il blocco esistente.  Uso: python scripts/rig_motion_inject.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ESCLUSE = re.compile(r'^(admin|bookmarklet)')

CSS = (
    '@media (prefers-reduced-motion:no-preference){'
    '@view-transition{navigation:auto}'
    '::view-transition-old(root){animation:rig-vt-out .4s cubic-bezier(.32,.72,0,1) both}'
    '::view-transition-new(root){animation:rig-vt-in .55s cubic-bezier(.32,.72,0,1) both}'
    'html{scroll-behavior:smooth}'
    '.sr,.sr-left,.sr-right,.rv{transition-duration:.95s;transition-timing-function:cubic-bezier(.32,.72,0,1)}'
    '}'
    '@keyframes rig-vt-out{to{opacity:0;transform:scale(.985)}}'
    '@keyframes rig-vt-in{from{opacity:0;transform:scale(1.015)}}'
)
BLOCCO = '<style id="rig-motion">' + CSS + '</style>'
ESISTENTE = re.compile(r'<style id="rig-motion">.*?</style>', re.S)

aggiornate = saltate = 0
for p in sorted(ROOT.glob('*.html')):
    if ESCLUSE.match(p.name):
        continue
    s = p.read_bytes().decode('utf-8')
    if ESISTENTE.search(s):
        nuovo = ESISTENTE.sub(BLOCCO, s, count=1)
    elif '</head>' in s:
        nuovo = s.replace('</head>', BLOCCO + '\n</head>', 1)
    else:
        saltate += 1
        print('senza </head>:', p.name)
        continue
    if nuovo != s:
        p.write_bytes(nuovo.encode('utf-8'))
        aggiornate += 1
print('pagine aggiornate:', aggiornate, '| saltate:', saltate)
