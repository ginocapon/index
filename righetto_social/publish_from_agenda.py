"""
Legge la tabella Supabase `pianificazioni` e pubblica in finestra vicina allo slot.

Facebook facebook_post: POST /{page-id}/feed con link + message.
Instagram instagram_feed: image_url da og:image del link.
Google Business (tipo google): localPosts API v4.
Con GBP_MIRROR_META=1 (default) replica post/reel Meta sulla scheda Google.

Variabili .env: SUPABASE_URL, SUPABASE_KEY (service_role sul server),
META_PAGE_ACCESS_TOKEN, META_PAGE_ID, META_IG_USER_ID,
GOOGLE_GBP_ACCESS_TOKEN, GOOGLE_GBP_PARENT (accounts/ID/locations/ID).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from supabase import Client, create_client

ROOT = Path(__file__).resolve().parent
_SCRIPTS = ROOT.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from righetto_immobile_slug import generate_property_slug, share_immobile_url

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
    cap = expand_spintax(sp) if sp else (row.get("titolo") or "Post").strip()
    link = (row.get("link_media") or "").strip()
    if link and link not in cap:
        cap = cap.rstrip() + "\n\n" + link
    tags = row.get("keywords") or []
    if isinstance(tags, list) and tags:
        tag_line = " ".join(str(t).strip() for t in tags if str(t).strip())
        if tag_line and tag_line not in cap:
            cap = cap.rstrip() + "\n\n" + tag_line
    return cap[:2200]


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


BASE_SITE = "https://righettoimmobiliare.it"
GBP_DEFAULT_IMAGE = f"{BASE_SITE}/img/og-default.webp"


def env_or_empty(name: str) -> str:
    return os.environ.get(name, "").strip()


def caption_for_gbp(row: dict[str, Any]) -> str:
    cap = caption_for_row(row)
    cap = re.sub(r"#\w+", "", cap)
    cap = re.sub(r"[ \t]+\n", "\n", cap)
    cap = re.sub(r"\n{3,}", "\n\n", cap).strip()
    return cap[:1500]


def gbp_credentials() -> tuple[str, str] | None:
    token = env_or_empty("GOOGLE_GBP_ACCESS_TOKEN")
    parent = env_or_empty("GOOGLE_GBP_PARENT")
    if not token or not parent:
        return None
    parent = parent.strip().strip("/")
    if not parent.startswith("accounts/"):
        parent = f"accounts/{parent}"
    return token, parent


def gbp_create_local_post(
    *,
    token: str,
    parent: str,
    summary: str,
    cta_url: str,
    image_url: str | None = None,
) -> dict[str, Any]:
    url = f"https://mybusiness.googleapis.com/v4/{parent}/localPosts"
    body: dict[str, Any] = {
        "languageCode": "it",
        "summary": summary[:1500],
        "topicType": "STANDARD",
        "callToAction": {
            "actionType": "LEARN_MORE",
            "url": cta_url[:2048],
        },
    }
    img = (image_url or "").strip()
    if img.startswith("http") and not img.lower().endswith(".mp4"):
        body["media"] = [{"mediaFormat": "PHOTO", "sourceUrl": img}]
    r = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=body,
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def mirror_meta_to_gbp(
    *,
    row: dict[str, Any],
    caption: str,
    url_page: str,
    media_direct: str,
) -> str | None:
    if env_or_empty("GBP_MIRROR_META") in ("0", "false", "no"):
        return None
    creds = gbp_credentials()
    if not creds:
        return None
    tipo = (row.get("tipo") or "").strip()
    if tipo not in ("facebook_post", "instagram_feed", "instagram_reel"):
        return None
    token, parent = creds
    cta = url_page or f"{BASE_SITE}/contatti"
    summary = caption_for_gbp(row) or caption or (row.get("titolo") or "Post")
    img = ""
    if media_direct.startswith("http") and not media_direct.lower().endswith(".mp4"):
        img = media_direct
    if not img:
        img = fetch_og_image(cta) or GBP_DEFAULT_IMAGE
    try:
        out = gbp_create_local_post(
            token=token,
            parent=parent,
            summary=summary,
            cta_url=cta,
            image_url=img,
        )
        return f"gbp_mirror={out.get('name', 'ok')}"
    except Exception as e:
        return f"gbp_mirror_err={str(e)[:120]}"


def slug_immobile(i: dict) -> str:
    return generate_property_slug(i)


def link_immobile_social(i: dict) -> str:
    return share_immobile_url(generate_property_slug(i))


def extract_public_url(row: dict[str, Any]) -> str:
    lm = (row.get("link_media") or "").strip()
    if lm.startswith("http"):
        return lm
    note = row.get("note") or ""
    m = re.search(r"https?://[^\s|]+", note)
    return (m.group(0).rstrip(".,)") if m else "").strip()


def resolve_public_url(sb: Client, row: dict[str, Any]) -> str:
    url = extract_public_url(row)
    if url:
        return url
    ref = (row.get("riferimento_id") or "").strip()
    contenuto = (row.get("contenuto") or "").strip().lower()
    if not ref:
        return ""
    try:
        if contenuto == "immobile" or (row.get("tipo") or "").startswith("instagram"):
            res = sb.table("immobili").select(
                "id,titolo,codice,slug,tipologia,categoria,tipo_operazione,comune"
            ).eq("id", ref).limit(1).execute()
            data = (res.data or [{}])[0]
            if data.get("id"):
                return link_immobile_social(data)
        res = sb.table("blog").select("id,slug,url_statico").eq("id", ref).limit(1).execute()
        data = (res.data or [{}])[0]
        if data.get("id"):
            slug = data.get("slug") or data.get("url_statico") or ""
            if slug:
                return f"{BASE_SITE}/blog-articolo?s={slug}"
    except Exception:
        return ""
    return ""


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


def row_matches_today(row: dict[str, Any], today: date) -> bool:
    try:
        di = date.fromisoformat(str(row["data_inizio"])[:10])
        df = date.fromisoformat(str(row["data_fine"])[:10])
    except (ValueError, TypeError):
        return False
    if not (di <= today <= df):
        return False
    py_to_js = {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}
    js_day = py_to_js.get(today.weekday(), 0)
    return js_day in giorni_list(row)


def due_for_cron(
    now: datetime, rows: list[dict[str, Any]], *, window_minutes: int
) -> list[dict[str, Any]]:
    return [
        r
        for r in rows
        if not already_handled(r.get("note"))
        and in_publish_window(now, r, window_minutes=window_minutes)
    ]


def due_for_manual(
    now: datetime,
    rows: list[dict[str, Any]],
    *,
    forza: bool = False,
    riprova_errati: bool = False,
) -> list[dict[str, Any]]:
    """Manuale: oggi, ora slot già passata (o --forza = tutto oggi non pubblicato)."""
    tz = now.tzinfo or ZoneInfo("Europe/Rome")
    today = now.date()
    out: list[dict[str, Any]] = []
    for r in rows:
        if already_handled(r.get("note"), allow_retry_error=riprova_errati):
            continue
        if not row_matches_today(r, today):
            continue
        if forza:
            out.append(r)
            continue
        slot = parse_time_local(tz, today, str(r.get("ora") or "12:00"))
        if now >= slot:
            out.append(r)
    return out


def already_handled(note: str | None, *, allow_retry_error: bool = False) -> bool:
    n = note or ""
    if PUB_OK in n:
        return True
    if PUB_ERR in n and not allow_retry_error:
        return True
    return False


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


def ig_media_publish_with_retry(
    *,
    version: str,
    ig_user_id: str,
    token: str,
    creation_id: str,
    max_wait_sec: int = 300,
    poll_sec: int = 15,
) -> dict[str, Any]:
    """
    Pubblica un container IG. Con token Pagina il GET status_code fallisce (auth 33);
    Meta consiglia di ripetere media_publish finché non esce 9007/2207027.
    """
    url_p = f"https://graph.facebook.com/{version}/{ig_user_id}/media_publish"
    deadline = time.time() + max_wait_sec
    last_body = ""
    while time.time() < deadline:
        r = requests.post(
            url_p,
            params={"access_token": token, "creation_id": creation_id},
            timeout=180,
        )
        if r.status_code == 200:
            return r.json()
        last_body = r.text
        err: dict[str, Any] = {}
        try:
            err = r.json().get("error") or {}
        except Exception:
            pass
        if err.get("code") == 9007 and err.get("error_subcode") == 2207027:
            time.sleep(poll_sec)
            continue
        r.raise_for_status()
    raise RuntimeError(
        f"IG media_publish timeout dopo {max_wait_sec}s: {last_body[:500]}"
    )


def ig_reel_create_and_publish(
    *,
    version: str,
    ig_user_id: str,
    token: str,
    caption: str,
    video_url: str,
) -> dict[str, Any]:
    url_m = f"https://graph.facebook.com/{version}/{ig_user_id}/media"
    r1 = requests.post(
        url_m,
        params={
            "access_token": token,
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption[:2200],
        },
        timeout=180,
    )
    r1.raise_for_status()
    cid = r1.json().get("id")
    if not cid:
        raise RuntimeError(f"IG reel media senza id: {r1.text}")

    pub = ig_media_publish_with_retry(
        version=version,
        ig_user_id=ig_user_id,
        token=token,
        creation_id=cid,
    )
    return {"container": r1.json(), "publish": pub}


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
        "--modo",
        choices=("cron", "manuale"),
        default="manuale",
        help="cron = Task Scheduler (finestra slot); manuale = tu decidi quando lanciare (default)",
    )
    parser.add_argument(
        "--id",
        dest="row_id",
        default="",
        help="Pubblica una sola riga agenda (UUID), subito",
    )
    parser.add_argument(
        "--forza",
        action="store_true",
        help="Manuale: anche slot il cui orario non è ancora arrivato",
    )
    parser.add_argument(
        "--riprova-errati",
        action="store_true",
        help="Riprova righe con PUB_ERR in note (es. dopo aver sistemato il token pagina)",
    )
    # Alias legacy
    parser.add_argument("--ignore-scheduler", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--ignore-window", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--window-minutes",
        type=int,
        default=int(os.environ.get("PUBLISH_WINDOW_MINUTES", "120")),
        help="Solo modo cron: minuti dopo l'ora slot (default 120)",
    )
    args = parser.parse_args()
    load_env()

    if args.ignore_scheduler or args.ignore_window:
        args.modo = "manuale"
        if args.ignore_window:
            args.forza = True

    tz_name = os.environ.get("AGENDA_TIMEZONE", "Europe/Rome")
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    today_iso = now.date().isoformat()

    if args.modo == "cron" and not args.dry_run and not args.row_id:
        if not respect_scheduler():
            print(
                "CRON: fuori finestra scheduler.py (config/settings.json).\n"
                "  Per pubblicare tu quando vuoi: python publish_from_agenda.py --modo manuale",
                file=sys.stderr,
            )
            return 3

    graph_v = os.environ.get("META_GRAPH_VERSION", "v21.0").strip()
    page_id = req_env("META_PAGE_ID")
    token = req_env("META_PAGE_ACCESS_TOKEN")
    ig_id = os.environ.get("META_IG_USER_ID", "").strip()

    sb = sb_client()

    if args.row_id:
        res = sb.table("pianificazioni").select("*").eq("id", args.row_id).limit(1).execute()
        due = res.data or []
        if not due:
            print(f"Riga non trovata: {args.row_id}", file=sys.stderr)
            return 1
        if already_handled(
            due[0].get("note"), allow_retry_error=args.riprova_errati
        ):
            print("Già pubblicata (PUB_OK in note).", file=sys.stderr)
            return 1
    else:
        rows = fetch_candidates(sb, today_iso)
        if args.modo == "cron":
            due = due_for_cron(now, rows, window_minutes=args.window_minutes)
        else:
            due = due_for_manual(
                now, rows, forza=args.forza, riprova_errati=args.riprova_errati
            )

    if not due:
        rows_n = len(fetch_candidates(sb, today_iso)) if not args.row_id else 0
        if args.modo == "cron":
            print(
                "CRON: nessuno slot in finestra ora.\n"
                f"  Oggi {today_iso}: {rows_n} righe in agenda.\n"
                "  Il cron ripete ogni 5–10 min nelle fasce settings.json."
            )
        else:
            print(
                "MANUALE: niente da pubblicare ora.\n"
                f"  Oggi {today_iso}: {rows_n} righe in agenda.\n"
                "  Pubblica dopo l'orario che hai messo in Agenda, oppure --forza."
            )
        return 0

    label = f"1 riga (id)" if args.row_id else f"{len(due)} righe — modo {args.modo}"
    print(f"Trovate {label} ({today_iso} {tz_name}).")

    exit_code = 0
    for row in due:
        rid = row.get("id")
        tipo = (row.get("tipo") or "").strip()
        titolo = (row.get("titolo") or "Post").strip()
        caption = caption_for_row(row)
        note = row.get("note") or ""
        url_page = resolve_public_url(sb, row)
        media_direct = (row.get("media_direct_url") or "").strip()

        if tipo == "instagram_story":
            msg = "Storia video non automatizzata in questo script."
            print(f"[skip] {rid}: {msg}")
            if not args.dry_run:
                patch_note(sb, rid, note, f" {PUB_ERR} {msg}")
            continue

        if tipo == "google":
            creds = gbp_credentials()
            if not creds:
                msg = (
                    "Google Business: configura GOOGLE_GBP_ACCESS_TOKEN e "
                    "GOOGLE_GBP_PARENT in .env (scheda Gruppo Immobiliare Righetto)."
                )
                print(f"[skip] {rid}: {msg}")
                if not args.dry_run:
                    patch_note(sb, rid, note, f" {PUB_ERR} {msg}")
                exit_code = max(exit_code, 4)
                continue

            cta_url = url_page or extract_public_url(row) or f"{BASE_SITE}/contatti"
            img = (
                media_direct
                if media_direct.startswith("http") and not media_direct.lower().endswith(".mp4")
                else fetch_og_image(cta_url) or GBP_DEFAULT_IMAGE
            )
            summary = caption_for_gbp(row) or titolo

            if args.dry_run:
                print(f"[dry-run] id={rid} tipo=google gbp cta={cta_url[:80]}…")
                continue

            try:
                gbp_token, gbp_parent = creds
                out = gbp_create_local_post(
                    token=gbp_token,
                    parent=gbp_parent,
                    summary=summary,
                    cta_url=cta_url,
                    image_url=img,
                )
                stamp = datetime.now(tz=ZoneInfo("UTC")).isoformat(timespec="seconds")
                patch_note(
                    sb,
                    rid,
                    note,
                    f" {PUB_OK} {stamp} gbp={out.get('name', 'ok')}",
                )
                print(f"[ok] id={rid} tipo=google gbp={out.get('name', 'ok')}")
            except requests.HTTPError as e:
                body = e.response.text if e.response is not None else str(e)
                err = f"GBP HTTP {body[:500]}"
                patch_note(sb, rid, note, f" {PUB_ERR} {err}")
                print(f"[err] id={rid}: {err}", file=sys.stderr)
                exit_code = max(exit_code, 5)
            except Exception as e:
                patch_note(sb, rid, note, f" {PUB_ERR} {e}")
                print(f"[err] id={rid}: {e}", file=sys.stderr)
                exit_code = max(exit_code, 5)
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

            elif tipo == "instagram_reel":
                if not ig_id:
                    raise RuntimeError("META_IG_USER_ID mancante")
                video = media_direct if media_direct.lower().endswith(".mp4") else ""
                if not video:
                    raise RuntimeError(
                        "Reel: media_direct_url deve essere .mp4 pubblico HTTPS "
                        "(genera con python genera_reel.py --pending)"
                    )
                out = ig_reel_create_and_publish(
                    version=graph_v,
                    ig_user_id=ig_id,
                    token=token,
                    caption=caption or titolo,
                    video_url=video,
                )
                parts_log.append(f"ig_reel={out.get('publish', {}).get('id', 'ok')}")

            else:
                msg = f"Tipo sconosciuto o non supportato: {tipo}"
                patch_note(sb, rid, note, f" {PUB_ERR} {msg}")
                print(f"[skip] {rid}: {msg}")
                continue

            gbp_extra = mirror_meta_to_gbp(
                row=row,
                caption=caption or titolo,
                url_page=url_page,
                media_direct=media_direct,
            )
            if gbp_extra:
                parts_log.append(gbp_extra)

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
