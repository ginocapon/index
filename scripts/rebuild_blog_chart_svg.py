# -*- coding: utf-8 -*-
"""Rigenera SVG chart-wrap: testo dentro i box, contrasto WCAG, frecce lineari."""
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

NOTE_KW = (
    "fascia",
    "fonte:",
    "analisi:",
    "schema qualitativo",
    "compenso",
    "padova e provincia",
    "non sostituisce",
    "metodo comparativo",
)
FOOTNOTE_FILL = "#152435"
SUBTITLE_FILL = "#3D4F63"
ARROW_STROKE = "#E85A20"


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
    if "FF6B35" in f or "E1DBD1" in f:
        return FOOTNOTE_FILL
    if "6B7A8D" in f:
        return FOOTNOTE_FILL if opacity else "#FFFFFF"
    return "#FFFFFF"


def _is_footnote_line(text: str) -> bool:
    low = text.lower()
    if len(text) > 28:
        return True
    return any(k in low for k in NOTE_KW)


def _walk(inner: str) -> list[tuple[str, object]]:
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

    def flush_rect() -> None:
        nonlocal pending_rect, pending_lines
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
                inside = t["y"] <= pending_rect["y"] + pending_rect["h"] * 0.92
                if inside:
                    pending_lines.append(t["content"])
                    continue
                flush_rect()
            if t["y"] >= 96 or _is_footnote_line(t["content"]):
                footnotes.append(t["content"])
            elif t["fill"] in ("#6B7A8D", "#556578", "rgba(255,255,255,.85)"):
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


def _normalize_steps(steps: list[dict], footnotes: list[str]) -> tuple[list[dict], list[str]]:
    fn = list(footnotes)
    for st in steps:
        primary = st["lines"][0]
        extras = st["lines"][1:]
        subs: list[str] = []
        for ex in extras:
            if _is_footnote_line(ex):
                fn.append(ex)
            elif len(ex) <= 22:
                subs.append(ex)
            else:
                fn.append(ex)
        st["lines"] = [primary] + subs[:1]
    return steps, fn


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


def _wrap_words(text: str, max_chars: int, max_lines: int = 2) -> list[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        prop = f"{cur} {w}".strip() if cur else w
        if len(prop) <= max_chars:
            cur = prop
        else:
            if cur:
                lines.append(cur)
            cur = w
        if len(lines) >= max_lines:
            break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if lines and len("".join(lines)) < len(text.replace(" ", "")) - 2:
        last = lines[-1]
        if len(last) > max_chars - 1:
            lines[-1] = last[: max_chars - 1] + "…"
        elif not last.endswith("…"):
            lines[-1] = last + "…"
    return lines or [text[: max(4, max_chars - 1)] + "…"]


def _marker_def(uid: int) -> str:
    mid = f"rigArr{uid}"
    return (
        f'<defs><marker id="{mid}" viewBox="0 0 12 12" refX="10" refY="6" '
        f'markerWidth="7" markerHeight="7" orient="auto" markerUnits="strokeWidth">'
        f'<path d="M1,1 L11,6 L1,11 Z" fill="{ARROW_STROKE}"/></marker></defs>'
    )


def _arrow(x1: float, x2: float, y: float, mid: str) -> str:
    if x2 <= x1 + 6:
        return ""
    return (
        f'<path d="M{x1:.0f} {y:.0f} H{x2:.0f}" stroke="{ARROW_STROKE}" '
        f'stroke-width="2.5" stroke-linecap="round" marker-end="url(#{mid})"/>'
    )


def _svg_box_text(
    uid: int,
    idx: int,
    x: float,
    y0: float,
    bw: float,
    bh: float,
    lines: list[str],
    fill: str,
    fs: int = 14,
) -> str:
    clip = f"rigClip{uid}_{idx}"
    max_chars = max(7, int(bw / (fs * 0.55)))
    wrapped: list[str] = []
    for ln in lines[:2]:
        wrapped.extend(_wrap_words(ln, max_chars, 1))
    wrapped = wrapped[:2]
    if len(wrapped) == 1 and len(wrapped[0]) > max_chars + 4:
        fs = max(11, fs - 2)
        max_chars = max(7, int(bw / (fs * 0.55)))
        wrapped = _wrap_words(lines[0], max_chars, 2)
    cx = x + bw / 2
    out = [
        f'<clipPath id="{clip}"><rect x="{x:.1f}" y="{y0:.1f}" '
        f'width="{bw:.1f}" height="{bh:.1f}" rx="10"/></clipPath>'
    ]
    if len(wrapped) == 1:
        ly = y0 + bh / 2 + fs / 3
        out.append(
            f'<text x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle" '
            f'clip-path="url(#{clip})" font-size="{fs}" font-weight="700" '
            f'fill="{fill}">{_esc(wrapped[0])}</text>'
        )
    else:
        out.append(
            f'<text x="{cx:.1f}" y="{y0 + bh / 2 - 4:.1f}" text-anchor="middle" '
            f'clip-path="url(#{clip})" fill="{fill}">'
        )
        for i, wl in enumerate(wrapped):
            fsi = fs if i == 0 else max(11, fs - 2)
            dy = "0" if i == 0 else str(fsi + 2)
            out.append(
                f'<tspan x="{cx:.1f}" dy="{dy}" font-size="{fsi}" '
                f'font-weight="700">{_esc(wl)}</tspan>'
            )
        out.append("</text>")
    return "".join(out)


def _footnote_lines(vb_w: float, y: float, lines: list[str]) -> tuple[float, str]:
    parts: list[str] = []
    max_chars = int(vb_w / 7.2)
    for raw in lines[:4]:
        for wl in _wrap_words(raw, max_chars, 3):
            parts.append(
                f'<text x="{vb_w / 2:.0f}" y="{y:.0f}" text-anchor="middle" '
                f'font-size="13" font-weight="600" fill="{FOOTNOTE_FILL}">'
                f"{_esc(wl)}</text>"
            )
            y += 18
    return y, "".join(parts)


def _flow_width(n: int) -> float:
    return float(min(960, max(700, 158 * n + 44)))


def _build_flow(title: str, steps: list[dict], footnotes: list[str], uid: int) -> tuple:
    n = len(steps)
    vb_w = _flow_width(n)
    mid = f"rigArr{uid}"
    margin, gap = 20, 28
    bw = (vb_w - 2 * margin - (n - 1) * gap) / n
    bh = 66
    y0 = 56
    parts = [_marker_def(uid)]
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="34" text-anchor="middle" font-size="18" '
        f'fill="{FOOTNOTE_FILL}" font-weight="700">{_esc(title)}</text>'
    )
    x = margin
    ay = y0 + bh / 2
    for i, st in enumerate(steps):
        op = f' opacity="{st["opacity"]}"' if st.get("opacity") else ""
        parts.append(
            f'<rect x="{x:.0f}" y="{y0}" width="{bw:.0f}" height="{bh}" '
            f'rx="10" fill="{st["fill"]}"{op}/>'
        )
        box_lines = [st["lines"][0]]
        parts.append(
            _svg_box_text(uid, i, x, y0, bw, bh, box_lines, st["label_fill"], 14)
        )
        if i < n - 1:
            parts.append(_arrow(x + bw + 3, x + bw + gap - 10, ay, mid))
        x += bw + gap
    fy = y0 + bh + 28
    fy, fn_svg = _footnote_lines(vb_w, fy, footnotes)
    parts.append(fn_svg)
    h = max(fy + 20, 210)
    return vb_w, h, "".join(parts)


def _build_timeline(title: str, steps: list[dict], footnotes: list[str], uid: int) -> tuple:
    vb_w = _flow_width(len(steps))
    mid = f"rigArr{uid}"
    n = len(steps)
    margin, gap = 18, 26
    bw = (vb_w - 2 * margin - (n - 1) * gap) / n
    bh = 54
    y0 = 54
    parts = [_marker_def(uid)]
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="34" text-anchor="middle" font-size="18" '
        f'fill="{FOOTNOTE_FILL}" font-weight="700">{_esc(title)}</text>'
    )
    x = margin
    ay = y0 + bh / 2
    for i, st in enumerate(steps):
        op = f' opacity="{st["opacity"]}"' if st.get("opacity") else ""
        parts.append(
            f'<rect x="{x:.0f}" y="{y0}" width="{bw:.0f}" height="{bh}" '
            f'rx="10" fill="{st["fill"]}"{op}/>'
        )
        parts.append(
            _svg_box_text(uid, i, x, y0, bw, bh, [st["lines"][0]], st["label_fill"], 15)
        )
        sub = st["lines"][1] if len(st["lines"]) > 1 else ""
        if sub:
            cx = x + bw / 2
            parts.append(
                f'<text x="{cx:.0f}" y="{y0 + bh + 18:.0f}" text-anchor="middle" '
                f'font-size="12" font-weight="600" fill="{SUBTITLE_FILL}">'
                f"{_esc(sub)}</text>"
            )
        if i < n - 1:
            parts.append(_arrow(x + bw + 3, x + bw + gap - 10, ay, mid))
        x += bw + gap
    fy = y0 + bh + 44
    fy, fn_svg = _footnote_lines(vb_w, fy, footnotes)
    parts.append(fn_svg)
    h = max(fy + 16, 230)
    return vb_w, h, "".join(parts)


def _is_light_fill(fill: str) -> bool:
    f = fill.upper()
    return "E1DBD1" in f or ("6B7A8D" in f and "2C" not in f)


def _build_two_column(title: str, steps: list[dict], footnotes: list[str], uid: int) -> tuple:
    vb_w = 580
    mid = f"rigArr{uid}"
    left, right = steps[0], steps[1]
    if _is_light_fill(right["fill"]) and not _is_light_fill(left["fill"]):
        left, right = right, left
    gap = 40
    bw = (vb_w - 36 - gap) / 2
    line_count = max(len(left["lines"]), len(right["lines"]))
    bh = max(108, 32 + 20 * min(line_count, 4))
    y0 = 50
    lx, rx = 18, 18 + bw + gap
    parts = [_marker_def(uid)]

    def col(x: float, st: dict, idx: int) -> None:
        op = f' opacity="{st["opacity"]}"' if st.get("opacity") else ""
        parts.append(
            f'<rect x="{x:.0f}" y="{y0}" width="{bw:.0f}" height="{bh}" '
            f'rx="12" fill="{st["fill"]}"{op}/>'
        )
        cx = x + bw / 2
        ty = y0 + 26
        for j, line in enumerate(st["lines"][:4]):
            fs = "16" if j == 0 else "14"
            parts.append(
                f'<text x="{cx:.0f}" y="{ty:.0f}" text-anchor="middle" '
                f'font-size="{fs}" font-weight="700" fill="{st["label_fill"]}">'
                f"{_esc(_wrap_words(line, int(bw / 7), 2)[0])}</text>"
            )
            ty += 20

    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="32" text-anchor="middle" font-size="18" '
        f'fill="{FOOTNOTE_FILL}" font-weight="700">{_esc(title)}</text>'
    )
    col(lx, left, 0)
    col(rx, right, 1)
    ay = y0 + bh / 2
    parts.append(_arrow(lx + bw + 4, rx - 12, ay, mid))
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="{ay + 4:.0f}" text-anchor="middle" '
        f'font-size="12" font-weight="700" fill="{SUBTITLE_FILL}">vs</text>'
    )
    fy = y0 + bh + 26
    fy, fn_svg = _footnote_lines(vb_w, fy, footnotes)
    parts.append(fn_svg)
    h = max(fy + 12, 250)
    return vb_w, h, "".join(parts)


def _build_h_bar(title: str, steps: list[dict], footnotes: list[str], uid: int) -> tuple:
    vb_w = 640
    parts = [_marker_def(uid)]
    parts.append(
        f'<text x="{vb_w / 2:.0f}" y="32" text-anchor="middle" font-size="18" '
        f'fill="{FOOTNOTE_FILL}" font-weight="700">{_esc(title)}</text>'
    )
    ordered = sorted(steps, key=lambda s: s.get("y_hint", 0))
    max_w = max(s["w_hint"] for s in ordered) or 1
    if max(s["w_hint"] for s in ordered) - min(s["w_hint"] for s in ordered) < 24:
        for i, st in enumerate(ordered):
            st = dict(st)
            st["w_hint"] = max_w * (1.0 - i * 0.14)
            ordered[i] = st
        max_w = max(s["w_hint"] for s in ordered) or 1
    label_w = 175
    bar_x = label_w + 14
    max_bar = vb_w - bar_x - 22
    y = 50
    row_h = 42
    for st in ordered:
        label = st["lines"][0]
        w = max(60, (st["w_hint"] / max_w) * max_bar)
        for j, wl in enumerate(_wrap_words(label, 26, 2)):
            parts.append(
                f'<text x="12" y="{y + 16 + j * 14:.0f}" font-size="12" '
                f'font-weight="700" fill="{FOOTNOTE_FILL}">{_esc(wl)}</text>'
            )
        parts.append(
            f'<rect x="{bar_x:.0f}" y="{y + 6:.0f}" width="{w:.0f}" height="{row_h - 14}" '
            f'rx="6" fill="{st["fill"]}"/>'
        )
        y += row_h
    fy = y + 12
    fy, fn_svg = _footnote_lines(vb_w, fy, footnotes)
    parts.append(fn_svg)
    h = max(fy + 12, 210)
    return vb_w, h, "".join(parts)


def _rebuild_svg(inner: str, uid: int, svg_title: str) -> str:
    title, steps, footnotes, _ = _extract(inner)
    steps, footnotes = _normalize_steps(steps, footnotes)
    if not steps:
        return ""
    kind = _classify(steps)
    dual = [s for s in steps if len(s["lines"]) >= 2 and len(s["lines"][1]) <= 22]
    if kind == "flow" and len(steps) >= 3 and len(dual) >= len(steps) // 2:
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
        f'<svg viewBox="0 0 {vb_w:.0f} {h:.0f}" width="100%" height="{int(h * 1.08)}" '
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
        path.write_text(new, encoding="utf-8")
        if new != raw:
            files += 1
            charts += c
            print(f"OK {path.name}: {c}")
    print(f"Rigenerati {charts} grafici in {files} file")


if __name__ == "__main__":
    main()
