#!/usr/bin/env python3
"""Genera op `replace` (ancore univoche) che correggono le frasi alterate da vecchie sostituzioni automatiche.

  python3 scripts/seo_auto/fix_text_artifacts.py blog-x.html            # stampa le op JSON
  python3 scripts/seo_auto/fix_text_artifacts.py blog-x.html --preview  # mostra prima → dopo

Le op vanno in data/seo-auto/approvals.json e si pubblicano con `seo_auto.py apply` (backup + rollback).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PADOVA_MAX = 8  # oltre questa soglia «a Padova» si alterna con «in città» (regola anti keyword stuffing)


def _cap(src: str, out: str) -> str:
    return out[0].upper() + out[1:] if src[:1].isupper() else out


def _rules(state: dict) -> list[tuple[str, object]]:
    def a_padova(m):
        if state["a_padova"] >= PADOVA_MAX:
            return _cap(m.group(0), "in città")
        state["a_padova"] += 1
        return _cap(m.group(0), "a Padova")

    def di_padova(m):
        return _cap(m.group(0), "della città" if state["a_padova"] >= PADOVA_MAX else "di Padova")

    def year(m):
        return f"a Padova nel {m.group(1)}"

    return [
        (r"\b[Nn]el capoluogo euganeo\b", a_padova),
        (r"\b[Aa]l capoluogo euganeo\b", a_padova),
        (r"\b[Dd]el capoluogo euganeo\b", di_padova),
        (r"\b[Dd]al capoluogo euganeo\b", lambda m: _cap(m.group(0), "da Padova")),
        (r"\b[Ss]ul capoluogo euganeo\b", lambda m: _cap(m.group(0), "su Padova")),
        (r"\b[Ii]l capoluogo euganeo\b", lambda m: "Padova"),
        (r"\bcapoluogo euganeo\b", lambda m: "Padova"),
        (r"\b[Nn]el territorio patavino\b", lambda m: _cap(m.group(0), "nel Padovano")),
        (r"\b[Dd]el territorio patavino\b", lambda m: _cap(m.group(0), "del Padovano")),
        (r"\b[Ii]l territorio patavino\b", lambda m: _cap(m.group(0), "il Padovano")),
        (r"\bterritorio patavino\b", lambda m: "territorio padovano"),
        (r"\bdi <strong>lo studio</strong>", lambda m: "di <strong>Righetto Immobiliare</strong>"),
        (r"\bdi lo studio\b", lambda m: "di Righetto Immobiliare"),
        (r"\b(elaborazion\w*) (?:de)?l?\s?il team\b", lambda m: f"{m.group(1)} Righetto Immobiliare"),
        (r"\bil team su dati\b", lambda m: "Righetto Immobiliare su dati"),
        (r"Comune del Padovano", lambda m: "Comune di Padova"),
        (r"\b(?:nel territorio|in provincia|nell'hinterland) (20\d\d)\b", year),
        (r"\binterne la nostra struttura\b", lambda m: "interne Righetto Immobiliare"),
        (r"\bnel comune nel (20\d\d)\b", lambda m: f"a Padova nel {m.group(1)}"),
        (r"principali zone locale", lambda m: "principali zone della città"),
        (r"\bZona padovano\b", lambda m: "Zona"),
    ]


def _anchor(t: str, s: int, e: int) -> tuple[int, int]:
    lo, hi = s, e
    while t.count(t[lo:hi]) > 1:
        lo, hi = max(0, lo - 12), min(len(t), hi + 12)
        if lo == 0 and hi == len(t):
            break
    return lo, hi


def build_ops(text: str) -> tuple[list[dict], list[tuple[str, str]]]:
    state = {"a_padova": len(re.findall(r"\ba Padova\b", text, re.I))}
    ops, preview = [], []
    for pat, fn in _rules(state):
        while True:
            m = re.search(pat, text)
            if not m:
                break
            new = fn(m)
            lo, hi = _anchor(text, m.start(), m.end())
            find = text[lo:hi]
            repl = text[lo:m.start()] + new + text[m.end():hi]
            ops.append({"op": "replace", "find": find, "html": repl})
            preview.append((m.group(0), new))
            text = text[:lo] + repl + text[hi:]
    return ops, preview


def main() -> None:
    f = ROOT / sys.argv[1]
    ops, preview = build_ops(f.read_text(encoding="utf-8"))
    if "--preview" in sys.argv:
        for a, b in preview:
            print(f"  {a!r} → {b!r}")
        print(f"{len(ops)} correzioni")
    else:
        print(json.dumps(ops, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
