# -*- coding: utf-8 -*-
"""Grafici chart-wrap blog: dimensioni, font, box allineati, frecce con marker."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG_RE = re.compile(
    r'(<figure class="chart-wrap"[^>]*>)(.*?)(</figure>)',
    re.I | re.S,
)
SVG_RE = re.compile(r"<svg\b([^>]*)>(.*?)</svg>", re.I | re.S)
RECT_RE = re.compile(r"<rect\b([^>]*)/?>", re.I)


def _scale_font(m: re.Match) -> str:
    n = int(m.group(1))
    return f'font-size="{max(13, round(n * 1.65))}"'


def _parse_vb_w(attrs: str) -> float:
    m = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?)', attrs)
    if m:
        return float(m.group(1))
    m = re.search(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', attrs)
    return float(m.group(1)) if m else 520.0


def _rect_fields(block: str) -> dict | None:
    def f(name: str, default: float = 0.0) -> float:
        mm = re.search(rf'\b{name}="([^"]+)"', block, re.I)
        return float(mm.group(1)) if mm else default

    w, h = f("width", 0), f("height", 0)
    if w < 36 or h < 20:
        return None
    return {"x": f("x"), "y": f("y"), "w": w, "h": h, "raw": block}


def redistribute_rects(inner: str, vb_w: float) -> str:
    """Allinea rettangoli orizzontali con gap uniforme (box allungati, no sovrapposizioni)."""
    matches = list(RECT_RE.finditer(inner))
    items: list[dict] = []
    for m in matches:
        parsed = _rect_fields(m.group(1))
        if not parsed:
            continue
        parsed["span"] = (m.start(), m.end(), m.group(0))
        items.append(parsed)
    if len(items) < 2:
        return inner
    items.sort(key=lambda i: i["x"])
    margin, gap = 16, 18
    n = len(items)
    total_w = sum(i["w"] for i in items)
    avail = max(vb_w - 2 * margin, total_w)
    scale = min(1.35, (avail - (n - 1) * gap) / total_w) if total_w else 1.0
    scale = max(scale, 0.85)
    x = margin
    out = inner
    for item in reversed(items):
        nw = item["w"] * scale
        new_rect = item["span"][2]
        new_rect = re.sub(r'\bx="[^"]+"', f'x="{x:.0f}"', new_rect, count=1)
        new_rect = re.sub(r'width="\d+"', f'width="{nw:.0f}"', new_rect, count=1)
        out = out[: item["span"][0]] + new_rect + out[item["span"][1] :]
        item["x"], item["w"] = x, nw
        x += nw + gap
    return out


def realign_text_to_rects(inner: str) -> str:
    rects: list[dict] = []
    for m in RECT_RE.finditer(inner):
        p = _rect_fields(m.group(1))
        if p:
            rects.append(p)
    if not rects:
        return inner

    def fix_text(m: re.Match) -> str:
        tag = m.group(1)
        xm = re.search(r'\bx="([^"]+)"', tag)
        if not xm or 'text-anchor="middle"' not in tag:
            return m.group(0)
        tx = float(xm.group(1))
        best = None
        best_d = 1e9
        for r in rects:
            cx = r["x"] + r["w"] / 2
            d = abs(tx - cx)
            if d < best_d and tx >= r["x"] - 30 and tx <= r["x"] + r["w"] + 30:
                best_d = d
                best = cx
        if best is None:
            return m.group(0)
        new_tag = re.sub(r'\bx="[^"]+"', f'x="{best:.0f}"', tag, count=1)
        return f"<text{new_tag}>{m.group(2)}</text>"

    return re.sub(r"<text\b([^>]*)>([^<]*)</text>", fix_text, inner, flags=re.I)


def _inject_marker(svg_inner: str, uid: int) -> str:
    mid = f"rigArr{uid}"
    marker = (
        f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="8" markerHeight="8" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 Z" fill="#FF6B35"/></marker>'
    )
    if f'id="{mid}"' not in svg_inner:
        if "<defs>" in svg_inner:
            if marker not in svg_inner:
                svg_inner = svg_inner.replace("<defs>", f"<defs>{marker}", 1)
        else:
            svg_inner = f"<defs>{marker}</defs>" + svg_inner
    svg_inner = re.sub(
        r'(<path\b[^>]*stroke="#FF6B35"[^>]*)(/?>)',
        lambda m: (
            m.group(1)
            + (' marker-end="url(#' + mid + ')"' if "marker-end" not in m.group(1) else "")
            + m.group(2)
        ),
        svg_inner,
        flags=re.I,
    )
    return svg_inner


def _flow_arrows_between_rects(inner: str, uid: int) -> str:
    """Aggiunge connettori tra rettangoli in fila se mancano."""
    if re.search(r'<path[^>]+stroke="#FF6B35"', inner, re.I):
        return inner
    rects: list[dict] = []
    for m in RECT_RE.finditer(inner):
        p = _rect_fields(m.group(1))
        if p:
            rects.append(p)
    if len(rects) < 2:
        return inner
    rects.sort(key=lambda r: r["x"])
    mid = f"rigArr{uid}"
    parts = []
    for i in range(len(rects) - 1):
        a, b = rects[i], rects[i + 1]
        y = a["y"] + a["h"] / 2
        x1 = a["x"] + a["w"] + 4
        x2 = b["x"] - 4
        if x2 > x1 + 8:
            parts.append(
                f'<path d="M{x1:.0f} {y:.0f} L{x2:.0f} {y:.0f}" stroke="#FF6B35" '
                f'stroke-width="3.5" marker-end="url(#{mid})"/>'
            )
    if not parts:
        return inner
    insert = inner.find("<rect")
    if insert < 0:
        return inner
    return inner[:insert] + "".join(parts) + inner[insert:]


def layout_fix_svg(svg_full: str, uid: int) -> str:
    m = SVG_RE.search(svg_full)
    if not m:
        return svg_full
    attrs, inner = m.group(1), m.group(2)
    vb_w = _parse_vb_w(attrs)
    inner = redistribute_rects(inner, vb_w)
    inner = realign_text_to_rects(inner)
    inner = _flow_arrows_between_rects(inner, uid)
    inner = _inject_marker(inner, uid)
    if "rig-chart-upgraded" not in attrs:
        attrs = attrs.strip() + ' class="rig-chart-svg rig-chart-upgraded"'
    return f"<svg {attrs.strip()}>{inner}</svg>"


def upgrade_svg_block(svg_full: str, uid: int) -> str:
    m = SVG_RE.search(svg_full)
    if not m:
        return svg_full
    if "rig-chart-upgraded" in m.group(1):
        return layout_fix_svg(svg_full, uid)
    attrs, inner = m.group(1), m.group(2)

    inner = re.sub(r'font-size="(\d+)"', _scale_font, inner)
    inner = re.sub(r'stroke-width="2"', 'stroke-width="3.5"', inner)
    inner = re.sub(r'stroke-width="2\.5"', 'stroke-width="3.5"', inner)

    def _rect_dim(tag: re.Match) -> str:
        s = tag.group(0)
        s = re.sub(
            r'width="(\d+)"',
            lambda x: f'width="{int(int(x.group(1)) * 1.28)}"',
            s,
            count=1,
        )
        s = re.sub(
            r'height="(\d+)"',
            lambda x: f'height="{int(int(x.group(1)) * 1.32)}"',
            s,
            count=1,
        )
        return s

    inner = re.sub(r"<rect\b[^/>]*/?>", _rect_dim, inner, flags=re.I)

    attrs = re.sub(r'\sclass="[^"]*"', "", attrs)
    attrs = attrs.strip() + ' class="rig-chart-svg rig-chart-upgraded"'

    def _vb(a: re.Match) -> str:
        w, h = float(a.group(1)), float(a.group(2))
        return f'viewBox="0 0 {int(w * 1.12)} {int(h * 1.38)}"'

    attrs = re.sub(r'viewBox="0 0 (\d+(?:\.\d+)?) (\d+(?:\.\d+)?)"', _vb, attrs)
    attrs = re.sub(
        r'height="(\d+)"',
        lambda a: f'height="{max(260, int(int(a.group(1)) * 1.65))}"',
        attrs,
    )
    if 'height="' not in attrs:
        attrs += ' height="280"'
    if 'width="' not in attrs:
        attrs = ' width="100%"' + attrs

    svg = f"<svg {attrs.strip()}>{inner}</svg>"
    return layout_fix_svg(svg, uid)


def process_html(text: str) -> tuple[str, int]:
    n = 0
    uid = 0

    def _fig(m: re.Match) -> str:
        nonlocal n, uid
        open_, body, close = m.group(1), m.group(2), m.group(3)
        sm = SVG_RE.search(body)
        if not sm:
            return m.group(0)
        uid += 1
        new_svg = upgrade_svg_block(sm.group(0), uid)
        if new_svg != sm.group(0):
            n += 1
        body = body[: sm.start()] + new_svg + body[sm.end() :]
        return open_ + body + close

    return FIG_RE.sub(_fig, text), n


def main() -> None:
    total_files = 0
    total_charts = 0
    for path in sorted(ROOT.glob("blog-*.html")):
        if "chart-wrap" not in path.read_text(encoding="utf-8"):
            continue
        raw = path.read_text(encoding="utf-8")
        new, c = process_html(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            total_files += 1
            total_charts += c
            print(f"OK {path.name}: {c} grafici")
    print(f"Fatto — {total_charts} chart aggiornati in {total_files} articoli")


if __name__ == "__main__":
    main()
