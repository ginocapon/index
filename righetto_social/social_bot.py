"""
Pubblicazione Facebook (Pagina) + Instagram (account collegato alla Pagina).
Richiede token Meta con permessi adeguati e account Instagram Business/Creator collegato.

Instagram foto da file locale: l'API richiede image_url pubblico HTTPS.
Per Facebook la foto può essere caricata dal disco (multipart).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parent


def load_settings() -> dict[str, Any]:
    path = ROOT / "config" / "settings.json"
    if not path.exists():
        print("Manca config/settings.json — copia settings.example.json e rinominalo.")
        sys.exit(2)
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def abs_content(rel: str) -> Path:
    return (ROOT / rel).resolve()


def scheduler_allows_publish(cfg: dict[str, Any]) -> bool:
    """Se scheduler.py restituisce 0, siamo in finestra oraria."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scheduler.py"), "--dry-run"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def publish_facebook_photo(
    *,
    graph_version: str,
    page_id: str,
    token: str,
    message: str,
    image_path: Path,
) -> dict[str, Any]:
    url = f"https://graph.facebook.com/{graph_version}/{page_id}/photos"
    with image_path.open("rb") as fh:
        files = {"source": fh}
        data = {"access_token": token, "message": message}
        r = requests.post(url, data=data, files=files, timeout=120)
    r.raise_for_status()
    return r.json()


def instagram_create_container(
    *,
    graph_version: str,
    ig_user_id: str,
    token: str,
    caption: str,
    image_url: str,
) -> str:
    url = f"https://graph.facebook.com/{graph_version}/{ig_user_id}/media"
    params = {
        "access_token": token,
        "caption": caption,
        "image_url": image_url,
    }
    r = requests.post(url, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    cid = data.get("id")
    if not cid:
        raise RuntimeError(f"Risposta IG media senza id: {data}")
    return str(cid)


def instagram_publish_container(
    *,
    graph_version: str,
    ig_user_id: str,
    token: str,
    creation_id: str,
) -> dict[str, Any]:
    url = f"https://graph.facebook.com/{graph_version}/{ig_user_id}/media_publish"
    params = {"access_token": token, "creation_id": creation_id}
    r = requests.post(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def pick_next_job(cfg: dict[str, Any]) -> tuple[Path, dict[str, Any]] | None:
    approvate = abs_content(cfg["paths"]["approvate"])
    if not approvate.exists():
        return None
    files = sorted(p for p in approvate.glob("*.json") if p.is_file())
    for p in files:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("stato") == "approvato" and data.get("pubblicato_il"):
            continue
        if data.get("stato") != "approvato":
            continue
        return p, data
    return None


def archive_job(job_path: Path, cfg: dict[str, Any], log: dict[str, Any]) -> None:
    pub = abs_content(cfg["paths"]["pubblicati"])
    pub.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    dest = pub / f"{job_path.stem}_{stamp}.json"
    payload = json.loads(job_path.read_text(encoding="utf-8"))
    payload["pubblicato_il"] = datetime.now(timezone.utc).isoformat()
    payload["log_pubblicazione"] = log
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    job_path.unlink()


def run_job(cfg: dict[str, Any], job_path: Path, data: dict[str, Any], *, dry_run: bool) -> None:
    meta = cfg["meta"]
    gv = meta["graph_api_version"]
    token = meta["page_access_token"]
    page_id = meta["page_id"]
    ig_id = meta["instagram_business_account_id"]

    message = (data.get("corpo") or "").strip()
    if data.get("titolo"):
        message = f"{data['titolo'].strip()}\n\n{message}".strip()

    media_rel = data.get("media_locale") or ""
    image_path = abs_content(cfg["paths"]["da_pubblicare"]) / Path(media_rel).name if media_rel else None
    if media_rel and image_path and not image_path.exists():
        image_path = ROOT / media_rel

    ig_url = (data.get("instagram_image_url") or "").strip()

    log: dict[str, Any] = {}

    if dry_run:
        print("[dry-run] Messaggio:", message[:200], "…" if len(message) > 200 else "")
        print("[dry-run] FB file:", image_path)
        print("[dry-run] IG URL:", ig_url or "(manca — richiesta URL pubblico)")
        return

    if data.get("pubblica_facebook", True):
        if not image_path or not image_path.exists():
            raise FileNotFoundError(f"Facebook: file immagine non trovato ({media_rel})")
        log["facebook"] = publish_facebook_photo(
            graph_version=gv,
            page_id=page_id,
            token=token,
            message=message,
            image_path=image_path,
        )

    if data.get("pubblica_instagram", True):
        if not ig_url:
            raise ValueError(
                "Instagram richiede instagram_image_url (HTTPS pubblico). "
                "Carica la foto sul tuo sito/CDN e incolla l'URL nella bozza."
            )
        cid = instagram_create_container(
            graph_version=gv,
            ig_user_id=ig_id,
            token=token,
            caption=message,
            image_url=ig_url,
        )
        log["instagram_container"] = {"id": cid}
        log["instagram_publish"] = instagram_publish_container(
            graph_version=gv,
            ig_user_id=ig_id,
            token=token,
            creation_id=cid,
        )

    archive_job(job_path, cfg, log)
    print("Pubblicazione completata; log in content/pubblicati/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bot pubblicazione Meta (Pagina + IG)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--ignore-scheduler", action="store_true", help="Pubblica anche fuori finestra")
    args = parser.parse_args()

    cfg = load_settings()
    if not args.ignore_scheduler and not args.dry_run:
        if not scheduler_allows_publish(cfg):
            print("Fuori finestra oraria (vedi scheduler.py). Usa --ignore-scheduler per forzare.")
            return 3

    picked = pick_next_job(cfg)
    if not picked:
        print("Nessun job approvato in content/approvate/")
        return 0

    job_path, data = picked
    try:
        run_job(cfg, job_path, data, dry_run=args.dry_run)
    except requests.HTTPError as e:
        print("Errore HTTP Meta:", e.response.text if e.response is not None else e)
        return 4
    except Exception as e:
        print("Errore:", e)
        return 5

    return 0


if __name__ == "__main__":
    sys.exit(main())
