# -*- coding: utf-8 -*-
"""
Pulizia graduale bucket Supabase foto-immobili dopo migrazione GitHub Pages.

Elimina solo file con copia locale verificata (manifest + file su disco).
NON tocca bucket documenti o planimetrie.

Uso:
  python scripts/purge_supabase_foto_immobili.py --dry-run
  python scripts/purge_supabase_foto_immobili.py --execute
  python scripts/purge_supabase_foto_immobili.py --execute --batch 40 --pause 2
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "media-manifest.json"
SUPABASE_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"
BUCKET = "foto-immobili"


def load_key() -> str:
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if key:
        return key
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("SUPABASE_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SUPABASE_KEY mancante")


def load_manifest() -> dict[str, str]:
    if not MANIFEST.is_file():
        return {}
    raw = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {k: v for k, v in raw.items() if not str(k).startswith("_") and isinstance(v, str)}


def local_exists(rel: str) -> bool:
    p = ROOT / rel.replace("/", os.sep)
    return p.is_file() and p.stat().st_size > 0


def resolve_local_path(storage_path: str, manifest: dict[str, str]) -> str | None:
    """Ritorna path img/ locale se migrato, altrimenti None."""
    sp = storage_path.lstrip("/")
    keys = [
        sp,
        f"{BUCKET}/{sp}",
        f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{sp}",
    ]
    for k in keys:
        rel = manifest.get(k)
        if rel and local_exists(rel):
            return rel

    # reel / blog video copiati con stesso nome
    name = Path(sp).name
    if sp.startswith("reels/"):
        cand = ROOT / "img" / "video" / "reels" / name
        if cand.is_file():
            return str(cand.relative_to(ROOT)).replace("\\", "/")
    if sp.startswith("blog/"):
        cand = ROOT / "img" / "video" / "blog" / name
        if cand.is_file():
            return str(cand.relative_to(ROOT)).replace("\\", "/")

    return None


def list_objects(key: str, prefix: str = "") -> list[str]:
    """Elenco ricorsivo path file nel bucket."""
    out: list[str] = []
    stack = [prefix]
    while stack:
        pre = stack.pop()
        body = json.dumps({"prefix": pre, "limit": 1000, "offset": 0}).encode()
        req = urllib.request.Request(
            f"{SUPABASE_URL}/storage/v1/object/list/{BUCKET}",
            data=body,
            method="POST",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                items = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"ERR list {pre!r}: {e.code}", file=sys.stderr)
            continue
        for item in items or []:
            name = (item.get("name") if isinstance(item, dict) else str(item)).strip()
            if not name:
                continue
            full = f"{pre}{name}" if not pre else f"{pre.rstrip('/')}/{name}"
            meta = item if isinstance(item, dict) else {}
            # cartella: id assente e metadata null, oppure name senza punto estensione in root listing
            if meta.get("id") is None and not Path(name).suffix:
                stack.append(full + "/")
            else:
                if Path(name).suffix or "/" in full:
                    out.append(full.lstrip("/"))
    return sorted(set(out))


def delete_batch(key: str, paths: list[str]) -> int:
    if not paths:
        return 0
    body = json.dumps({"prefixes": paths}).encode()
    req = urllib.request.Request(
        f"{SUPABASE_URL}/storage/v1/object/{BUCKET}",
        data=body,
        method="DELETE",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        r.read()
    return len(paths)


def fetch_db_supabase_urls(key: str) -> set[str]:
    """URL/path Supabase ancora referenziati in immobili.foto."""
    refs: set[str] = set()
    rows = json.loads(
        urllib.request.urlopen(
            urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/immobili?select=foto,planimetrie",
                headers={"apikey": key, "Authorization": f"Bearer {key}"},
            ),
            timeout=120,
        ).read().decode()
    )
    for row in rows:
        for field in ("foto", "planimetrie"):
            val = row.get(field)
            if isinstance(val, list):
                for u in val:
                    u = str(u)
                    if "supabase.co" in u or u.endswith((".jpg", ".png", ".webp", ".mp4")):
                        refs.add(u.split("/")[-1].split("?")[0])
            elif isinstance(val, str) and val:
                refs.add(val.split("/")[-1].split("?")[0])
    return refs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--batch", type=int, default=50, help="File per batch")
    ap.add_argument("--pause", type=float, default=1.5, help="Secondi tra batch")
    ap.add_argument("--max-batches", type=int, default=0, help="0 = tutti")
    args = ap.parse_args()
    if not args.dry_run and not args.execute:
        ap.error("Specifica --dry-run o --execute")

    key = load_key()
    manifest = load_manifest()
    print(f"Manifest: {len(manifest)} voci")

    all_objs = list_objects(key)
    print(f"Oggetti in {BUCKET}: {len(all_objs)}")

    safe: list[str] = []
    skip: list[str] = []
    for obj in all_objs:
        if resolve_local_path(obj, manifest):
            safe.append(obj)
        else:
            skip.append(obj)

    db_refs = fetch_db_supabase_urls(key) if args.execute or args.dry_run else set()
    orphans: list[str] = []
    for obj in skip:
        fname = Path(obj).name
        if fname not in db_refs:
            orphans.append(obj)

    print(f"Eliminabili (backup GitHub OK): {len(safe)}")
    print(f"Orfani (vecchie versioni, non in DB): {len(orphans)}")
    print(f"Saltati (ancora in DB o senza copia): {len(skip) - len(orphans)}")
    if skip and len(skip) - len(orphans) > 0:
        kept = [s for s in skip if Path(s).name in db_refs]
        for s in kept[:5]:
            print(f"  KEEP {s}")

    to_delete = safe + orphans

    if args.dry_run:
        print(f"\n[dry-run] Eliminerei {len(safe)} + {len(orphans)} orfani = {len(safe) + len(orphans)} file")
        return 0

    deleted = 0
    batches = 0
    total = len(to_delete)
    for i in range(0, total, args.batch):
        if args.max_batches and batches >= args.max_batches:
            print(f"Stop: max-batches {args.max_batches}")
            break
        chunk = to_delete[i : i + args.batch]
        try:
            n = delete_batch(key, chunk)
            deleted += n
            batches += 1
            print(f"Batch {batches}: eliminati {n} ({deleted}/{total})")
        except urllib.error.HTTPError as e:
            print(f"ERR delete batch: {e.code} {e.read().decode()[:200]}", file=sys.stderr)
            return 1
        if i + args.batch < total:
            time.sleep(args.pause)

    remaining = list_objects(key)
    print(f"\nCompletato: {deleted} file rimossi da Supabase {BUCKET}")
    print(f"Oggetti residui nel bucket: {len(remaining)}")
    print("Bucket documenti e planimetrie: NON toccati")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
