"""
Legge la tabella Supabase `pianificazioni` e pubblica in finestra vicina allo slot.

Facebook facebook_post: POST /{page-id}/feed con link + message.
Instagram instagram_feed: image_url da og:image del link.

Variabili .env: SUPABASE_URL, SUPABASE_KEY (service_role sul server),
META_PAGE_ACCESS_TOKEN, META_PAGE_ID, META_IG_USER_ID.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from supabase import Client, create_client

ROOT = Path(__file__).resolve().parent

PUB_OK = "| PUB_OK:"
PUB_ERR = "| PUB_ERR:"

UA = "Mozilla/5.0 (compatible; RighettoAgendaBot/1.0; +https://righettoimmobiliare.it)"


def expand_spintax(text: str) -> str:
    """Sostituisce {a|b|c} con una variante (prima opzione = stabile per cron)."""
    if not text:
        return text

    def repl(m: re.Match[str]) -> str:
        parts = [p.strip() for p in m.group(1).split("|") if p.strip()]
        return parts[0] if parts else ""

    prev = None
    out = text
    while prev != out:
        prev = out
        out = re.sub(r"\{([^{}]+)\}", repl, out)
    return out


def caption_for_row(row: dict[str, Any]) -> str:
    sp = (row.get("corpo_spintax") or "").strip()
    if sp:
        return expand_spintax(sp)[:2200]
    return (row.get("titolo") or "Post").strip()[:2200]


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def req_env(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        print(f"Manca variabile d'ambiente {name}", file=sys.stderr)
        sys.exit(2)
    return v


def sb_client() -> Client:
    url = req_env("SUPABASE_URL")
    key = req_env("SUPABASE_KEY")
    return create_client(url, key)


def extract_public_url(row: dict[str, Any]) -> str:
    lm = (row.get("link_media") or "").strip()
    if lm.startswith("http"):
        return lm
    note = row.get("note") or ""
    m = re.search(r"https?://[^\s|]+", note)
    return (m.group(0).rstrip(".,)") if m else "").strip()


def fetch_og_image(page_url: str, timeout: float = 20.0) -> str | None:
    try:
        r = requests.get(page_url, headers={"User-Agent": UA}, timeout=timeout)
        r.raise_for_status()
        html = r.text
    except requests.RequestException:
        return None
    for pattern in (
        r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']',
        r'<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:image["\']',
    ):
        m = re.search(pattern, html, re.I)
        if m:
            return m.group(1).strip()
    return None


def giorni_list(row: dict[str, Any]) -> list[int]:
    g = row.get("giorni")
    if isinstance(g, list):
        return [int(x) for x in g]
    return []


def parse_time_local(tz: ZoneInfo, d: date, ora_str: str) -> datetime:
    parts = (ora_str or "12:00").split(":")
    h = int(parts[0]) if parts else 12
    m = int(parts[1]) if len(parts) > 1 else 0
    return datetime(d.year, d.month, d.day, h, m, 0, tzinfo=tz)


def in_publish_window(
    now: datetime, row: dict[str, Any], *, window_minutes: int
) -> bool:
    tz = now.tzinfo or ZoneInfo("Europe/Rome")
    today = now.date()
    try:
        di = date.fromisoformat(str(row["data_inizio"])[:10])
        df = date.fromisoformat(str(row["data_fine"])[:10])
    except (ValueError, TypeError):
        return False
    if not (di <= today <= df):
        return False
    py_to_js = {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}
    js_day = py_to_js.get(today.weekday(), 0)
    if js_day not in giorni_list(row):
        return False
    slot = parse_time_local(tz, today, str(row.get("ora") or "12:00"))
    win_end = slot + timedelta(minutes=window_minutes)
    return slot <= now <= win_end


def already_handled(note: str | None) -> bool:
    n = note or ""
    return PUB_OK in n or PUB_ERR in n


def graph_feed_post(
    *,
    version: str,
    page_id: str,
    token: str,
    message: str,
    link: str,
) -> dict[str, Any]:
    url = f"https://graph.facebook.com/{version}/{page_id}/feed"
    data = {
        "access_token": token,
        "message": message[:2000],
        "link": link,
    }
    r = requests.post(url, data=data, timeout=60)
    r.raise_for_status()
    return r.json()


def ig_create_and_publish(
    *,
    version: str,
    ig_user_id: str,
    token: str,
    caption: str,
    image_url: str,
) -> dict[str, Any]:
    url_m = f"https://graph.facebook.com/{version}/{ig_user_id}/media"
    r1 = requests.post(
        url_m,
        params={
            "access_token": token,
            "caption": caption[:2200],
            "image_url": image_url,
        },
        timeout=90,
    )
    r1.raise_for_status()
    cid = r1.json().get("id")
    if not cid:
        raise RuntimeError(f"IG media senza id: {r1.text}")

    url_p = f"https://graph.facebook.com/{version}/{ig_user_id}/media_publish"
    r2 = requests.post(
        url_p,
        params={"access_token": token, "creation_id": cid},
        timeout=90,
    )
    r2.raise_for_status()
    return {"container": r1.json(), "publish": r2.json()}


def patch_note(sb: Client, row_id: Any, note: str, suffix: str) -> None:
    new_note = (note or "").strip() + suffix
    sb.table("pianificazioni").update(
        {"note": new_note, "updated_at": datetime.now(tz=ZoneInfo("UTC")).isoformat()}
    ).eq("id", row_id).execute()


def fetch_candidates(sb: Client, today_iso: str) -> list[dict[str, Any]]:
    q = (
        sb.table("pianificazioni")
        .select("*")
        .lte("data_inizio", today_iso)
        .gte("data_fine", today_iso)
        .execute()
    )
    return q.data or []


def respect_scheduler() -> bool:
    proc = __import__("subprocess").run(
        [sys.executable, str(ROOT / "scheduler.py"), "--dry-run"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Pubblica da agenda Supabase → Meta")
    parser.add_argument("--dry-run", action="store_true", help="Solo elenco cosa farebbe")
    parser.add_argument(
        "--ignore-scheduler",
        action="store_true",
        help="Ignora finestra oraria scheduler.py",
    )
    parser.add_argument(
        "--window-minutes",
        type=int,
        default=int(os.environ.get("PUBLISH_WINDOW_MINUTES", "120")),
        help="Finestra dopo l'orario slot (default 120)",
    )
    args = parser.parse_args()
    load_env()

    tz_name = os.environ.get("AGENDA_TIMEZONE", "Europe/Rome")
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    today_iso = now.date().isoformat()

    if not args.ignore_scheduler and not args.dry_run:
        if not respect_scheduler():
            print(
                "Fuori finestra oraria (scheduler.py). "
                "Usa --ignore-scheduler per forzare.",
                file=sys.stderr,
            )
            return 3

    graph_v = os.environ.get("META_GRAPH_VERSION", "v21.0").strip()
    page_id = req_env("META_PAGE_ID")
    token = req_env("META_PAGE_ACCESS_TOKEN")
    ig_id = os.environ.get("META_IG_USER_ID", "").strip()

    sb = sb_client()
    rows = fetch_candidates(sb, today_iso)
    due = [r for r in rows if in_publish_window(now, r, window_minutes=args.window_minutes)]
    due = [r for r in due if not already_handled(r.get("note"))]

    if not due:
        print("Nessuna pianificazione in finestra o già marcata PUB_OK/PUB_ERR.")
        return 0

    print(f"Trovate {len(due)} righe in finestra ({today_iso} {tz_name}).")

    exit_code = 0
    for row in due:
        rid = row.get("id")
        tipo = (row.get("tipo") or "").strip()
        titolo = (row.get("titolo") or "Post").strip()
        caption = caption_for_row(row)
        note = row.get("note") or ""
        url_page = extract_public_url(row)
        media_direct = (row.get("media_direct_url") or "").strip()

        if tipo in ("instagram_story", "instagram_reel"):
            msg = f"Tipo {tipo} non automatizzato in questo script (serve video/API dedicate)."
            print(f"[skip] {rid}: {msg}")
            if not args.dry_run:
                patch_note(sb, rid, note, f" {PUB_ERR} {msg}")
            continue

        if tipo == "google":
            msg = "Google Business non gestito qui."
            print(f"[skip] {rid}: {msg}")
            continue

        if tipo == "blog":
            msg = "Tipo blog calendar=CMS — salta pubblicazione Meta."
            print(f"[skip] {rid}: {msg}")
            continue

        if not url_page:
            msg = "URL pubblico mancante (link_media o note con https)."
            print(f"[err] {rid}: {msg}")
            if not args.dry_run:
                patch_note(sb, rid, note, f" {PUB_ERR} {msg}")
            exit_code = max(exit_code, 4)
            continue

        if args.dry_run:
            print(f"[dry-run] id={rid} tipo={tipo} url={url_page[:80]}…")
            continue

        try:
            parts_log: list[str] = []
            if tipo == "facebook_post":
                out = graph_feed_post(
                    version=graph_v,
                    page_id=page_id,
                    token=token,
                    message=caption or titolo,
                    link=url_page,
                )
                parts_log.append(f"fb={out.get('id','ok')}")

            elif tipo == "instagram_feed":
                if not ig_id:
                    raise RuntimeError("META_IG_USER_ID mancante")
                img = media_direct if media_direct.startswith("http") else None
                if not img:
                    img = fetch_og_image(url_page)
                if not img:
                    raise RuntimeError(
                        "Immagine mancante: media_direct_url o og:image dalla pagina"
                    )
                out = ig_create_and_publish(
                    version=graph_v,
                    ig_user_id=ig_id,
                    token=token,
                    caption=caption or titolo,
                    image_url=img,
                )
                parts_log.append(f"ig={out.get('publish', {}).get('id', 'ok')}")

            else:
                msg = f"Tipo sconosciuto o non supportato: {tipo}"
                patch_note(sb, rid, note, f" {PUB_ERR} {msg}")
                print(f"[skip] {rid}: {msg}")
                continue

            stamp = datetime.now(tz=ZoneInfo("UTC")).isoformat(timespec="seconds")
            patch_note(sb, rid, note, f" {PUB_OK} {stamp} {' '.join(parts_log)}")
            print(f"[ok] id={rid} tipo={tipo} {' '.join(parts_log)}")
        except requests.HTTPError as e:
            body = e.response.text if e.response is not None else str(e)
            err = f"HTTP {body[:500]}"
            patch_note(sb, rid, note, f" {PUB_ERR} {err}")
            print(f"[err] id={rid}: {err}", file=sys.stderr)
            exit_code = max(exit_code, 5)
        except Exception as e:
            patch_note(sb, rid, note, f" {PUB_ERR} {e}")
            print(f"[err] id={rid}: {e}", file=sys.stderr)
            exit_code = max(exit_code, 5)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
