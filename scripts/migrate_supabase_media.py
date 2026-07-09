# -*- coding: utf-8 -*-
"""
Migra foto e video da Supabase Storage a GitHub Pages (img/).

Riduce egress: le immagini annunci e i reel passano su righettoimmobiliare.it/img/…

Uso:
  python scripts/migrate_supabase_media.py --dry-run
  python scripts/migrate_supabase_media.py --photos
  python scripts/migrate_supabase_media.py --photos --update-db
  python scripts/migrate_supabase_media.py --videos
  python scripts/migrate_supabase_media.py --visite
  python scripts/migrate_supabase_media.py --codice LP0286

Richiede SUPABASE_KEY in .env (service_role per --update-db).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_IMMOBILI = ROOT / "img" / "immobili"
IMG_PLAN = ROOT / "img" / "planimetrie"
IMG_VIDEO_REELS = ROOT / "img" / "video" / "reels"
IMG_VIDEO_BLOG = ROOT / "img" / "video" / "blog"
MANIFEST_PATH = ROOT / "data" / "media-manifest.json"
VISITE_PATH = ROOT / "data" / "visite-virtuali.json"
SITE = "https://righettoimmobiliare.it"
SUPABASE_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"
BUCKET_FOTO = "foto-immobili"
BUCKET_PLAN = "planimetrie"


def load_key() -> str:
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if key:
        return key
    env = ROOT / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("SUPABASE_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SUPABASE_KEY mancante in .env")


def sb_get(path: str, key: str) -> list | dict:
    url = f"{SUPABASE_URL}{path}"
    req = urllib.request.Request(
        url,
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def sb_patch_immobile(row_id: str, payload: dict, key: str) -> None:
    url = f"{SUPABASE_URL}/rest/v1/immobili?id=eq.{row_id}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="PATCH",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    with urllib.request.urlopen(req, timeout=60):
        pass


def storage_public_url(bucket: str, path: str) -> str:
    return f"{SUPABASE_URL}/storage/v1/object/public/{bucket}/{path.lstrip('/')}"


def extract_storage_path(url: str) -> tuple[str, str] | None:
    """Ritorna (bucket, path) da URL Supabase storage."""
    if not url or not isinstance(url, str):
        return None
    u = url.strip()
    m = re.search(r"/storage/v1/object/public/([^/]+)/(.+)$", u)
    if m:
        return m.group(1), m.group(2).split("?")[0]
    if u.startswith("foto-immobili/"):
        return BUCKET_FOTO, u.split("?", 1)[0]
    if u.startswith("planimetrie/"):
        return BUCKET_PLAN, u.split("?", 1)[0]
    if u.startswith("reels/") or u.startswith("blog/"):
        return BUCKET_FOTO, u.split("?", 1)[0]
    return None


def slugify_name(name: str) -> str:
    base = Path(name).stem.lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return base[:60] or "foto"


def download_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "RighettoMediaMigrate/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def to_webp(src: Path, dest: Path) -> bool:
    """Converte in WebP se Pillow disponibile, altrimenti copia originale."""
    try:
        from PIL import Image  # type: ignore

        img = Image.open(src)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        max_w = 1600
        if img.width > max_w:
            ratio = max_w / img.width
            img = img.resize((max_w, int(img.height * ratio)), Image.Resampling.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, "WEBP", quality=82, method=4)
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"  WARN WebP {src.name}: {e}", file=sys.stderr)
        return False


def save_media(
    url: str,
    dest_rel: str,
    *,
    dry_run: bool,
    manifest: dict,
) -> str | None:
    """Scarica e salva; ritorna path relativo img/…"""
    parsed = extract_storage_path(url)
    if not parsed:
        return None
    bucket, spath = parsed
    if bucket not in (BUCKET_FOTO, BUCKET_PLAN):
        return None

    local_rel = dest_rel.replace("\\", "/")
    if local_rel.startswith(SITE):
        local_rel = local_rel.replace(SITE + "/", "")
    dest_abs = ROOT / local_rel

    if dry_run:
        print(f"  [dry] {url[:80]} -> {local_rel}")
        manifest[url] = local_rel
        manifest[spath] = local_rel
        manifest[f"{bucket}/{spath}"] = local_rel
        return local_rel

    if dest_abs.is_file() and dest_abs.stat().st_size > 0:
        manifest[url] = local_rel
        manifest[spath] = local_rel
        manifest[f"{bucket}/{spath}"] = local_rel
        return local_rel

    public = storage_public_url(bucket, spath)
    try:
        raw = download_bytes(public)
    except urllib.error.HTTPError as e:
        print(f"  ERR download {public}: {e.code}", file=sys.stderr)
        return None

    dest_abs.parent.mkdir(parents=True, exist_ok=True)
    ext = Path(spath).suffix.lower() or ".jpg"
    tmp = dest_abs.with_suffix(ext)
    tmp.write_bytes(raw)

    webp_rel = str(Path(local_rel).with_suffix(".webp")).replace("\\", "/")
    webp_abs = ROOT / webp_rel
    if ext in (".jpg", ".jpeg", ".png", ".webp") and to_webp(tmp, webp_abs):
        tmp.unlink(missing_ok=True)
        local_rel = webp_rel
    else:
        shutil.move(str(tmp), str(dest_abs))
        local_rel = dest_rel.replace("\\", "/")

    manifest[url] = local_rel
    manifest[spath] = local_rel
    manifest[f"{bucket}/{spath}"] = local_rel
    print(f"  OK {local_rel}")
    return local_rel


def migrate_immobile_photos(
    row: dict,
    *,
    dry_run: bool,
    manifest: dict,
    update_db: bool,
    key: str,
) -> int:
    codice = (row.get("codice") or row.get("id") or "unknown").strip()
    codice_safe = re.sub(r"[^A-Za-z0-9_-]", "", codice) or "unknown"
    foto_raw = row.get("foto") or row.get("foto_urls") or []
    if not isinstance(foto_raw, list):
        return 0

    new_foto: list[str] = []
    changed = 0
    for idx, u in enumerate(foto_raw):
        u = str(u or "").strip()
        if not u:
            continue
        if u.startswith("img/") or u.startswith(SITE + "/img/"):
            new_foto.append(u.replace(SITE + "/", "").lstrip("/"))
            continue
        if not extract_storage_path(u) and not u.startswith("http"):
            new_foto.append(u)
            continue
        fname = slugify_name(u.split("/")[-1])
        dest = f"img/immobili/{codice_safe}/{idx + 1:03d}-{fname}.webp"
        local = save_media(u, dest, dry_run=dry_run, manifest=manifest)
        if local:
            new_foto.append(local)
            changed += 1
        else:
            new_foto.append(u)

    if changed and update_db and not dry_run:
        payload: dict = {"foto": new_foto}
        try:
            sb_patch_immobile(str(row["id"]), payload, key)
            print(f"  DB aggiornato: {codice_safe} ({len(new_foto)} foto)")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:300]
            print(f"  ERR DB {codice_safe}: {e.code} {body}", file=sys.stderr)

    return changed


def migrate_videos(*, dry_run: bool, manifest: dict, key: str) -> int:
    """Scarica reel/blog da bucket foto-immobili/reels/ e blog/."""
    n = 0
    for prefix, out_dir in (("reels", IMG_VIDEO_REELS), ("blog", IMG_VIDEO_BLOG)):
        try:
            items = sb_get(
                f"/storage/v1/object/list/{BUCKET_FOTO}",
                key,
            )
        except Exception:
            items = []
        # list API needs POST body for prefix — use storage list via REST
        list_url = f"{SUPABASE_URL}/storage/v1/object/list/{BUCKET_FOTO}"
        body = json.dumps({"prefix": prefix, "limit": 200}).encode("utf-8")
        req = urllib.request.Request(
            list_url,
            data=body,
            method="POST",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                items = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            print(f"WARN list {prefix}: {e}", file=sys.stderr)
            continue

        for item in items or []:
            name = (item.get("name") if isinstance(item, dict) else str(item)).strip()
            if not name or name.endswith("/"):
                continue
            spath = f"{prefix}/{name}"
            url = storage_public_url(BUCKET_FOTO, spath)
            dest_rel = f"img/video/{prefix}/{name}"
            dest_abs = ROOT / dest_rel
            if dry_run:
                print(f"  [dry] video {spath} -> {dest_rel}")
                manifest[url] = dest_rel
                n += 1
                continue
            if dest_abs.is_file():
                manifest[url] = dest_rel
                continue
            try:
                dest_abs.parent.mkdir(parents=True, exist_ok=True)
                dest_abs.write_bytes(download_bytes(url))
                manifest[url] = dest_rel
                print(f"  OK video {dest_rel}")
                n += 1
            except Exception as e:
                print(f"  ERR video {spath}: {e}", file=sys.stderr)
    return n


def migrate_visite(*, dry_run: bool, manifest: dict) -> int:
    if not VISITE_PATH.is_file():
        return 0
    data = json.loads(VISITE_PATH.read_text(encoding="utf-8"))
    changed = 0
    if isinstance(data, list):
        tours = data
    elif isinstance(data, dict):
        tours = list(data.values())
    else:
        return 0

    for tour in tours:
        if not isinstance(tour, dict):
            continue
        codice = re.sub(r"[^A-Za-z0-9_-]", "", (tour.get("codice") or tour.get("id") or "vt"))
        scenes = tour.get("scenes") or tour.get("stanze") or []
        for si, sc in enumerate(scenes):
            img = (sc.get("img") or sc.get("url") or "").strip()
            if not img or img.startswith("img/"):
                continue
            # Riusa file gia migrato in img/immobili/{codice}/ se presente nel manifest
            mapped = manifest.get(img) or manifest.get(img.split("/")[-1])
            if mapped and not dry_run:
                sc["img"] = mapped
                changed += 1
                print(f"  OK visite {codice} scene {si + 1} -> {mapped}")
                continue
            dest = f"img/immobili/{codice}/vt-{si + 1:02d}-{slugify_name(img)}.webp"
            local = save_media(img, dest, dry_run=dry_run, manifest=manifest)
            if local:
                sc["img"] = local
                changed += 1
        cover = (tour.get("cover") or "").strip()
        if cover and not cover.startswith("img/"):
            mapped = manifest.get(cover) or manifest.get(cover.split("/")[-1])
            if mapped and not dry_run:
                tour["cover"] = mapped
                changed += 1
            else:
                dest = f"img/immobili/{codice}/vt-cover.webp"
                local = save_media(cover, dest, dry_run=dry_run, manifest=manifest)
                if local:
                    tour["cover"] = local
                    changed += 1
    if changed and not dry_run:
        VISITE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  visite-virtuali.json aggiornato ({changed} URL)")
    return changed


def load_manifest() -> dict:
    if MANIFEST_PATH.is_file():
        raw = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            return {k: v for k, v in raw.items() if not k.startswith("_")}
    return {}


def save_manifest(manifest: dict) -> None:
    out = {
        "_meta": {
            "description": "Mappa URL Supabase → path locale img/",
            "updated": datetime.now(timezone.utc).isoformat(),
            "count": len(manifest),
        },
        **manifest,
    }
    MANIFEST_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Manifest: {MANIFEST_PATH} ({len(manifest)} voci)")


def run_sync_og() -> None:
    script = ROOT / "scripts" / "sync_og_immobili.py"
    if script.is_file():
        print("Rigenero share-immobile-*.html …")
        subprocess.run([sys.executable, str(script)], cwd=str(ROOT), check=False)


def main() -> int:
    ap = argparse.ArgumentParser(description="Migra media Supabase → img/ GitHub Pages")
    ap.add_argument("--dry-run", action="store_true", help="Solo anteprima, nessun file/DB")
    ap.add_argument("--photos", action="store_true", help="Migra foto immobili")
    ap.add_argument("--videos", action="store_true", help="Migra reel/video da Storage")
    ap.add_argument("--visite", action="store_true", help="Migra visite virtuali JSON")
    ap.add_argument("--update-db", action="store_true", help="PATCH immobili.foto su Supabase")
    ap.add_argument("--sync-og", action="store_true", help="Rigenera share-immobile dopo migrazione")
    ap.add_argument("--codice", help="Solo un immobile (codice)")
    args = ap.parse_args()

    if not any([args.photos, args.videos, args.visite]):
        args.photos = True

    key = load_key()
    manifest = load_manifest()
    dry = args.dry_run

    if args.photos:
        rows = sb_get(
            "/rest/v1/immobili?select=*&order=created_at.desc",
            key,
        )
        if args.codice:
            rows = [r for r in rows if (r.get("codice") or "").upper() == args.codice.upper()]
        print(f"Immobili da processare: {len(rows)}")
        total = 0
        for row in rows:
            cod = row.get("codice") or row.get("id")
            print(f"\n{cod}:")
            total += migrate_immobile_photos(
                row,
                dry_run=dry,
                manifest=manifest,
                update_db=args.update_db,
                key=key,
            )
        print(f"\nFoto migrate/verificate: {total}")

    if args.videos:
        print("\nVideo/reel:")
        migrate_videos(dry_run=dry, manifest=manifest, key=key)

    if args.visite:
        print("\nVisite virtuali:")
        migrate_visite(dry_run=dry, manifest=manifest)

    if not dry:
        save_manifest(manifest)
        if args.sync_og:
            run_sync_og()
    else:
        print(f"\n[dry-run] Manifest avrebbe {len(manifest)} voci. Riesegui senza --dry-run.")

    print("\nProssimi passi:")
    print("  1. git add img/ data/media-manifest.json")
    print("  2. python scripts/migrate_supabase_media.py --photos --update-db --sync-og")
    print("  3. commit + push -> GitHub Pages serve img/ senza egress Supabase")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
