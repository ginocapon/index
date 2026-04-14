# -*- coding: utf-8 -*-
"""Inserisce FAQ visibile (details) prima del CTA e corregge chiusura hero errata nelle zona-*.html."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERO_BAD = "</section></div>\n  </div>\n</section>"
HERO_OK = "</section>"

MARKER = "<!-- CTA -->"


def extract_faq_json_ld(html: str) -> dict | None:
    for m in re.finditer(
        r'<script\s+type="application/ld\+json">\s*(\{[\s\S]*?\})\s*</script>',
        html,
        re.IGNORECASE,
    ):
        chunk = m.group(1)
        if '"FAQPage"' not in chunk and "'FAQPage'" not in chunk:
            continue
        try:
            data = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if data.get("@type") == "FAQPage" and data.get("mainEntity"):
            return data
    return None


def build_visible_faq_section(data: dict, zone_label: str) -> str:
    items = data.get("mainEntity") or []
    rows = []
    for ent in items:
        if not isinstance(ent, dict) or ent.get("@type") != "Question":
            continue
        q = ent.get("name") or ""
        ans = (ent.get("acceptedAnswer") or {})
        a = ans.get("text") if isinstance(ans, dict) else ""
        if not q or not a:
            continue
        q_esc = q.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        a_esc = a.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        rows.append(
            f'      <details class="zona-faq-item"><summary>{q_esc}</summary><div class="zona-faq-a">{a_esc}</div></details>'
        )
    if not rows:
        return ""
    inner = "\n".join(rows)
    return f"""<!-- FAQ visibile (AEO) — allineata a JSON-LD FAQPage -->
<section class="sec zona-faq-visibile" id="faq-zona" aria-labelledby="faq-zona-h">
  <div class="sec-inner">
    <h2 class="sec-t" id="faq-zona-h">Domande frequenti su <strong>{zone_label}</strong></h2>
    <p class="zona-faq-lead">Risposte sintetiche sul quartiere e sul mercato: utili per chi cerca casa a Padova e per i motori di ricerca.</p>
    <div class="zona-faq-list">
{inner}
    </div>
  </div>
</section>

"""


def zone_title_from_filename(name: str) -> str:
    base = name.replace("zona-", "").replace(".html", "")
    return base.replace("-", " ").title()


def process_file(path: Path) -> tuple[bool, str]:
    html = path.read_text(encoding="utf-8")
    changed = False
    if HERO_BAD in html:
        html = html.replace(HERO_BAD, HERO_OK, 1)
        changed = True
    if 'class="zona-faq-visibile"' in html and MARKER in html:
        return changed, "skip-faq-present"
    data = extract_faq_json_ld(html)
    if not data or MARKER not in html:
        return changed, "skip-no-faq-or-marker"
    label = zone_title_from_filename(path.name)
    block = build_visible_faq_section(data, label)
    if not block:
        return changed, "skip-empty-faq"
    html = html.replace(MARKER, block + MARKER, 1)
    changed = True
    # CSS once per file
    css = """
    .zona-faq-visibile .zona-faq-lead{font-size:.86rem;line-height:1.75;color:var(--grigio);max-width:720px;margin-bottom:1.4rem}
    .zona-faq-list{max-width:800px}
    .zona-faq-item{border:1px solid var(--gc);border-radius:6px;margin-bottom:.55rem;background:#fff}
    .zona-faq-item summary{cursor:pointer;padding:.95rem 1.1rem;font-weight:600;font-size:.86rem;list-style:none}
    .zona-faq-item summary::-webkit-details-marker{display:none}
    .zona-faq-a{padding:0 1.1rem 1rem;font-size:.84rem;line-height:1.75;color:var(--grigio)}
"""
    if ".zona-faq-visibile" not in html:
        html = html.replace("</style>", css + "\n  </style>", 1)
        changed = True
    path.write_text(html, encoding="utf-8")
    return changed, "ok"


def main() -> int:
    files = sorted(ROOT.glob("zona-*.html"))
    if not files:
        print("Nessun zona-*.html in", ROOT)
        return 1
    for p in files:
        ch, msg = process_file(p)
        print(f"{p.name}: {msg}" + (" (hero fix)" if ch and msg != "ok" else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
