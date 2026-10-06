# -*- coding: utf-8 -*-
"""Rigenera SVG in figure.chart-wrap: box allineati, testo grassetto centrato, frecce corrette."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG_RE = re.compile(
    r'(<figure class="chart-wrap"[^>]*>)(.*?)(</figure>)',
    re.I | re.S,
)
SVG_RE = re.compile(r"<svg\b([^>]*)>(.*?)</svg>", re.I | re.S)
RECT_OPEN = re.compile(r"<rect\b([^>]*)/?>", re.I)
TEXT_EL = re.compile(r"<text\b([^>]*)>([^<]*)</text>", re.I)
PATH_EL = re.compile(r"<path\b[^>]*(?:/>|>[^<]*</path>)", re.I)
TITLE_EL = re.compile(r"<title>([^<]*)</title>", re.I)

VB_W_DEFAULT = 640


def _attr(block: str, name: str, default: str = "") -> str:
    m = re.search(rf'\b{name}="([^"]*)"', block, re.I)
    return m.group(1) if m else default


def _float(block: str, name: str, default: float = 0.0) -> float:
    v = _attr(block, name, "")
    try:
        return float(v) if v else default
    except ValueError:
        return default


def _parse_rect(block: str) -> dict:
    return {
        "x": _float(block, "x"),
        "y": _float(block, "y"),
        "w": _float(block, "width"),
        "h": _float(block, "height"),
        "fill": _attr(block, "fill", "#2C4A6E"),
        "rx": _attr(block, "rx", "10"),
        "opacity": _attr(block, "opacity", ""),
    }


def _parse_text(block: str, content: str) -> dict:
    fs = _float(block, "font-size", 13)
    return {
        "x": _float(block, "x"),
        "y": _float(block, "y"),
        "content": content.strip(),
        "font_size": fs,
        "font_weight": _attr(block, "font-weight", ""),
        "fill": _attr(block, "fill", "#152435"),
        "anchor": _attr(block, "text-anchor", ""),
    }


def _label_fill_for_rect(fill: str, opacity: str) -> str:
    f = fill.upper()
    if "FF6B35" in f or "E1DBD1" in f or opacity:
        return "#152435"
    if "6B7A8D" in f and opacity:
        return "#152435"
    return "#FFFFFF"


def _walk(inner: str) -> list[tuple[str, object]]:
    """Ordine documento: rect, text (path/title ignorati per estrazione)."""
    out: list[tuple[str, object]] = []
    pos = 0
    while pos < len(inner):
        chunk = inner[pos:]
        if chunk.lstrip().startswith("<title"):
            m = TITLE_EL.match(inner, pos)
            if m:
                out.append(("title", m.group(1).strip()))
                pos = m.end()
                continue
        m = RECT_OPEN.match(inner, pos)
        if m:
            out.append(("rect", _parse_rect(m.group(1))))
            pos = m.end()
            continue
        m = TEXT_EL.match(inner, pos)
        if m:
            out.append(("text", _parse_text(m.group(1), m.group(2))))
            pos = m.end()
            continue
        m = PATH_EL.match(inner, pos)
        if m:
            pos = m.end()
            continue
        pos += 1
    return out


def _extract(inner: str) -> tuple[str, list[dict], list[str], str]:
    """title, steps[{lines, fill, opacity, label_fill}], footnotes, svg_title."""
    svg_title = ""
    for kind, data in _walk(inner):
        if kind == "title":
            svg_title = data
            break

    title = ""
    steps: list[dict] = []
    footnotes: list[str] = []
    pending_rect: dict | None = None
    pending_lines: list[str] = []
    pending_meta: dict | None = None

    def flush_rect() -> None:
        nonlocal pending_rect, pending_lines, pending_meta
        if pending_rect is None:
            return
        lines = [ln for ln in pending_lines if ln]
        if not lines:
            lines = ["—"]
        steps.append(
            {
                "lines": lines,
                "fill": pending_rect["fill"],
                "opacity": pending_rect["opacity"],
                "label_fill": _label_fill_for_rect(
                    pending_rect["fill"], pending_rect["opacity"]
                ),
                "w_hint": pending_rect["w"],
                "h_hint": pending_rect["h"],
                "y_hint": pending_rect["y"],
            }
        )
        pending_rect = None
        pending_lines = []
        pending_meta = None

    for kind, data in _walk(inner):
        if kind == "title":
            continue
        if kind == "text":
            t = data
            if not t["content"]:
                continue
            if (
                not title
                and t["y"] < 48
                and (t["font_weight"] == "700" or t["font_size"] >= 14)
            ):
                title = t["content"]
                continue
            if pending_rect is not None:
                inside = t["y"] <= pending_rect["y"] + pending_rect["h"] + 8
                below = (
                    pending_rect["y"] + pending_rect["h"]
                    < t["y"]
                    <= pending_rect["y"] + pending_rect["h"] + 28
                )
                if inside or below or len(pending_lines) == 0:
                    pending_lines.append(t["content"])
                    continue
            if t["y"] >= 100 or t["fill"] in ("#6B7A8D", "#556578"):
                footnotes.append(t["content"])
            elif not title and t["y"] < 48:
                title = t["content"]
            else:
                footnotes.append(t["content"])
        elif kind == "rect":
            flush_rect()
            pending_rect = data

    flush_rect()
    if not title and steps:
        title = svg_title or "Schema"
    return title, steps, footnotes, svg_title


def _classify(steps: list[dict]) -> str:
    if not steps:
        return "empty"
    hs = [s["h_hint"] for s in steps]
    ws = [s["w_hint"] for s in steps]
    ys = [round(s.get("y_hint", 0)) for s in steps]
    long_labels = sum(1 for s in steps if len(s["lines"][0]) > 20)
    if len(steps) == 2 and min(hs) >= 42 and min(ws) >= 120:
        return "two_column"
    if len(steps) >= 3 and (max(hs) <= 42 and len(set(ys)) >= 2 or long_labels >= 2):
        return "h_bar"
    if len(steps) >= 2 and max(hs) <= 75:
        return "flow"
    return "flow"


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _marker(uid: int) -> str:
    mid = f"rigArr{uid}"
    return (
        f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="8" markerHeight="8" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 Z" fill="#FF6B35"/></marker></defs>'
    )


def _arrow(x1: float, x2: float, y: float, mid: str) -> str:
    return (
        f'<path d="M{x1:.0f} {y:.0f} L{x2:.0f} {y:.0f}" stroke="#FF6B35" '
        f'stroke-width="3.5" marker-end="url(#{mid})"/>'
    )


def _build_flow(title: str, steps: list[dict], footnotes: list[str], uid: int) -> str:
    vb_w = VB_W_DEFAULT
    mid = f"rigArr{uid}"
    n = len(steps)
    margin, gap = 18, 22
    bw = (vb_w - 2 * margin - (n - 1) * gap) / n
    bh = 58
    y0 = 54
    cy = y0 + bh / 2 + 5
    parts = [_marker(uid)]
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="32" text-anchor="middle" font-size="18" '
        f'fill="#152435" font-weight="700">{_esc(title)}</text>'
    )
    x = margin
    for i, st in enumerate(steps):
        op = f' opacity="{st["opacity"]}"' if st.get("opacity") else ""
        parts.append(
            f'<rect x="{x:.0f}" y="{y0}" width="{bw:.0f}" height="{bh}" '
            f'rx="10" fill="{st["fill"]}"{op}/>'
        )
        cx = x + bw / 2
        lines = st["lines"]
        lf = st["label_fill"]
        if len(lines) == 1:
            parts.append(
                f'<text x="{cx:.0f}" y="{cy:.0f}" text-anchor="middle" '
                f'font-size="15" font-weight="700" fill="{lf}">{_esc(lines[0])}</text>'
            )
        else:
            parts.append(
                f'<text x="{cx:.0f}" y="{y0 + 24:.0f}" text-anchor="middle" '
                f'font-size="14" font-weight="700" fill="{lf}">{_esc(lines[0])}</text>'
            )
            parts.append(
                f'<text x="{cx:.0f}" y="{y0 + 42:.0f}" text-anchor="middle" '
                f'font-size="12" font-weight="600" fill="{lf}">{_esc(lines[1])}</text>'
            )
        if i < n - 1:
            parts.append(_arrow(x + bw + 2, x + bw + gap - 2, y0 + bh / 2, mid))
        x += bw + gap
    fy = y0 + bh + 32
    for fn in footnotes[:3]:
        parts.append(
            f'<text x="{vb_w / 2:.0f}" y="{fy:.0f}" text-anchor="middle" '
            f'font-size="14" fill="#556578">{_esc(fn)}</text>'
        )
        fy += 22
    h = max(fy + 16, 200)
    return vb_w, h, "".join(parts)


def _build_timeline(title: str, steps: list[dict], footnotes: list[str], uid: int) -> str:
    """4+ fasi con sottotitolo sotto il box."""
    vb_w = VB_W_DEFAULT
    mid = f"rigArr{uid}"
    n = len(steps)
    margin, gap = 16, 20
    bw = (vb_w - 2 * margin - (n - 1) * gap) / n
    bh = 52
    y0 = 52
    parts = [_marker(uid)]
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="32" text-anchor="middle" font-size="18" '
        f'fill="#152435" font-weight="700">{_esc(title)}</text>'
    )
    x = margin
    for i, st in enumerate(steps):
        op = f' opacity="{st["opacity"]}"' if st.get("opacity") else ""
        parts.append(
            f'<rect x="{x:.0f}" y="{y0}" width="{bw:.0f}" height="{bh}" '
            f'rx="10" fill="{st["fill"]}"{op}/>'
        )
        cx = x + bw / 2
        head = st["lines"][0]
        sub = st["lines"][1] if len(st["lines"]) > 1 else ""
        lf = st["label_fill"]
        parts.append(
            f'<text x="{cx:.0f}" y="{y0 + 32:.0f}" text-anchor="middle" '
            f'font-size="15" font-weight="700" fill="{lf}">{_esc(head)}</text>'
        )
        if sub:
            parts.append(
                f'<text x="{cx:.0f}" y="{y0 + bh + 20:.0f}" text-anchor="middle" '
                f'font-size="13" font-weight="600" fill="#556578">{_esc(sub)}</text>'
            )
        if i < n - 1:
            parts.append(_arrow(x + bw + 2, x + bw + gap - 2, y0 + bh / 2, mid))
        x += bw + gap
    fy = y0 + bh + 48
    for fn in footnotes[:2]:
        parts.append(
            f'<text x="{vb_w / 2:.0f}" y="{fy:.0f}" text-anchor="middle" '
            f'font-size="14" fill="#556578">{_esc(fn)}</text>'
        )
        fy += 22
    h = max(fy + 12, 220)
    return vb_w, h, "".join(parts)


def _is_light_fill(fill: str) -> bool:
    f = fill.upper()
    return "E1DBD1" in f or ("6B7A8D" in f and "2C" not in f)


def _build_two_column(title: str, steps: list[dict], footnotes: list[str], uid: int) -> str:
    vb_w = 560
    mid = f"rigArr{uid}"
    left, right = steps[0], steps[1]
    if _is_light_fill(right["fill"]) and not _is_light_fill(left["fill"]):
        left, right = right, left
    gap = 36
    bw = (vb_w - 40 - gap) / 2
    bh = max(100, 28 + 22 * max(len(left["lines"]), len(right["lines"])))
    y0 = 48
    lx, rx = 20, 20 + bw + gap
    parts = [_marker(uid)]
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="30" text-anchor="middle" font-size="18" '
        f'fill="#152435" font-weight="700">{_esc(title)}</text>'
    )

    def col(x: float, st: dict) -> None:
        op = f' opacity="{st["opacity"]}"' if st.get("opacity") else ""
        parts.append(
            f'<rect x="{x:.0f}" y="{y0}" width="{bw:.0f}" height="{bh}" '
            f'rx="12" fill="{st["fill"]}"{op}/>'
        )
        cx = x + bw / 2
        ty = y0 + 28
        for j, line in enumerate(st["lines"][:4]):
            fw = "700" if j == 0 else "600"
            fs = "16" if j == 0 else "14"
            parts.append(
                f'<text x="{cx:.0f}" y="{ty:.0f}" text-anchor="middle" '
                f'font-size="{fs}" font-weight="{fw}" fill="{st["label_fill"]}">'
                f"{_esc(line)}</text>"
            )
            ty += 20

    col(lx, left)
    col(rx, right)
    ay = y0 + bh / 2
    parts.append(_arrow(lx + bw + 4, rx - 4, ay, mid))
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="{ay + 5:.0f}" text-anchor="middle" '
        f'font-size="13" font-weight="700" fill="#556578">vs</text>'
    )
    fy = y0 + bh + 28
    for fn in footnotes[:2]:
        parts.append(
            f'<text x="{vb_w / 2:.0f}" y="{fy:.0f}" text-anchor="middle" '
            f'font-size="14" fill="#556578">{_esc(fn)}</text>'
        )
        fy += 22
    h = max(fy + 12, 240)
    return vb_w, h, "".join(parts)


def _build_h_bar(title: str, steps: list[dict], footnotes: list[str], uid: int) -> str:
    vb_w = 620
    parts = [_marker(uid)]
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="30" text-anchor="middle" font-size="18" '
        f'fill="#152435" font-weight="700">{_esc(title)}</text>'
    )
    ordered = sorted(steps, key=lambda s: s.get("y_hint", 0))
    max_w = max(s["w_hint"] for s in ordered) or 1
    if max(s["w_hint"] for s in ordered) - min(s["w_hint"] for s in ordered) < 24:
        for i, st in enumerate(ordered):
            st = dict(st)
            st["w_hint"] = max_w * (1.0 - i * 0.14)
            ordered[i] = st
        max_w = max(s["w_hint"] for s in ordered) or 1
    label_w = 168
    bar_x = label_w + 12
    max_bar = vb_w - bar_x - 20
    y = 48
    row_h = 40
    for st in ordered:
        label = st["lines"][0]
        w = max(56, (st["w_hint"] / max_w) * max_bar)
        parts.append(
            f'<text x="12" y="{y + 22:.0f}" font-size="13" font-weight="700" '
            f'fill="#152435">{_esc(label)}</text>'
        )
        parts.append(
            f'<rect x="{bar_x:.0f}" y="{y + 4:.0f}" width="{w:.0f}" height="{row_h - 10}" '
            f'rx="6" fill="{st["fill"]}"/>'
        )
        y += row_h
    fy = y + 16
    for fn in footnotes[:2]:
        parts.append(
            f'<text x="{vb_w / 2:.0f}" y="{fy:.0f}" text-anchor="middle" '
            f'font-size="14" fill="#556578">{_esc(fn)}</text>'
        )
        fy += 20
    h = max(fy + 12, 200)
    return vb_w, h, "".join(parts)


def _rebuild_svg(inner: str, uid: int, svg_title: str) -> str:
    title, steps, footnotes, _ = _extract(inner)
    if not steps:
        return ""
    kind = _classify(steps)
    # Timeline: molte fasi con 2 righe di testo
    dual = sum(1 for s in steps if len(s["lines"]) >= 2)
    if kind == "flow" and len(steps) >= 3 and dual >= len(steps) // 2:
        kind = "timeline"
    if kind == "two_column":
        vb_w, h, body = _build_two_column(title, steps, footnotes, uid)
    elif kind == "h_bar":
        vb_w, h, body = _build_h_bar(title, steps, footnotes, uid)
    elif kind == "timeline":
        vb_w, h, body = _build_timeline(title, steps, footnotes, uid)
    else:
        vb_w, h, body = _build_flow(title, steps, footnotes, uid)
    st = svg_title or title
    return (
        f'<svg viewBox="0 0 {vb_w} {h:.0f}" width="100%" height="{int(h * 1.05)}" '
        f'role="img" class="rig-chart-svg rig-chart-rebuilt">'
        f"<title>{_esc(st)}</title>{body}</svg>"
    )


def process_html(text: str) -> tuple[str, int]:
    n = 0
    uid = 0

    def _fig(m: re.Match) -> str:
        nonlocal n, uid
        open_, body, close = m.group(1), m.group(2), m.group(3)
        if "<table" in body.lower() and "<svg" not in body.lower():
            return m.group(0)
        sm = SVG_RE.search(body)
        if not sm:
            return m.group(0)
        uid += 1
        new_svg = _rebuild_svg(sm.group(2), uid, "")
        if not new_svg:
            return m.group(0)
        n += 1
        body = body[: sm.start()] + new_svg + body[sm.end() :]
        return open_ + body + close

    return FIG_RE.sub(_fig, text), n


def main() -> None:
    files = 0
    charts = 0
    for path in sorted(ROOT.glob("blog-*.html")):
        raw = path.read_text(encoding="utf-8")
        if "chart-wrap" not in raw or "<svg" not in raw:
            continue
        new, c = process_html(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            files += 1
            charts += c
            print(f"OK {path.name}: {c}")
    print(f"Rigenerati {charts} grafici in {files} file")


if __name__ == "__main__":
    main()
