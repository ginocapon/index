"""
Sposta una bozza da bozze_generate/ a content/approvate/ (creata se manca)
o marca il file JSON come approvato per il bot.
Uso interattivo da terminale.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOZZE = ROOT / "content" / "bozze_generate"
APPROVATE = ROOT / "content" / "approvate"


def list_bozze() -> list[Path]:
    if not BOZZE.exists():
        return []
    return sorted(p for p in BOZZE.glob("*.json") if p.is_file())


def approve(path: Path) -> Path:
    APPROVATE.mkdir(parents=True, exist_ok=True)
    dest = APPROVATE / path.name
    shutil.move(str(path), str(dest))
    data = json.loads(dest.read_text(encoding="utf-8"))
    data["stato"] = "approvato"
    dest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def main() -> int:
    bozze = list_bozze()
    if not bozze:
        print("Nessun file .json in content/bozze_generate/")
        return 1

    print("Bozze disponibili:")
    for i, p in enumerate(bozze, start=1):
        print(f"  [{i}] {p.name}")

    try:
        choice = input("Numero da approvare (invio per annullare): ").strip()
    except EOFError:
        return 1

    if not choice:
        print("Annullato.")
        return 0

    idx = int(choice)
    if idx < 1 or idx > len(bozze):
        print("Selezione non valida.")
        return 1

    dest = approve(bozze[idx - 1])
    print(f"OK → {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
