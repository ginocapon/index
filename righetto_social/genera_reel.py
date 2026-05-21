"""
Genera Reel Instagram (MP4 1080x1920) da foto immobili / blog / landing.
Richiede FFmpeg installato: https://ffmpeg.org/download.html

Uso:
  python genera_reel.py --pending
  python genera_reel.py --bozza-id UUID
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from postgrest.exceptions import APIError
from supabase import Client, create_client

ROOT = Path(__file__).resolve().parent
OUT_LOCAL = ROOT / "generated-reels"
BASE_SITE = "https://righettoimmobiliare.it"
TZ = ZoneInfo("Europe/Rome")
UA = "Mozilla/5.0 (compatible; RighettoReelGen/1.0; +https://righettoimmobiliare.it)"
BG = "0x1a2744"
SEC_PER_SLIDE = 4
MAX_IMAGES = 4


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def req_env(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        print(f"Manca {name} in .env", file=sys.stderr)
        sys.exit(2)
    return v


def sb_client() -> Client:
    return create_client(req_env("SUPABASE_URL"), req_env("SUPABASE_KEY"))


def find_ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if path:
        return path
    for candidate in (
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
    ):
        if Path(candidate).is_file():
            return candidate
    print(
        "FFmpeg non trovato. Installalo e aggiungilo al PATH:\n"
        "  winget install ffmpeg\n"
        "  oppure https://www.gyan.dev/ffmpeg/builds/",
        file=sys.stderr,
    )
    sys.exit(2)


def resolve_image_url(url: str, supabase_url: str) -> str:
    u = (url or "").strip()
    if not u:
        return ""
    if u.startswith(("http://", "https://", "data:")):
        return u
    path = u.lstrip("/")
    if path.startswith("foto-immobili/") or "/" in path and not path.startswith("img/"):
        return f"{supabase_url.rstrip('/')}/storage/v1/object/public/{path}"
    return f"{BASE_SITE.rstrip('/')}/{path}"


def fetch_og_image(page_url: str) -> str | None:
    try:
        r = requests.get(page_url, headers={"User-Agent": UA}, timeout=25)
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


def _valid_page_url(link: str | None) -> str | None:
    u = (link or "").strip()
    if not u.startswith("http"):
        return None
    if re.search(r"[?&]s=\s*$", u) or u.endswith("s="):
        return None
    return u


def _immobile_photos(sb: Client, ref: str, supabase_url: str) -> list[str]:
    out: list[str] = []
    row = sb.table("immobili").select("foto,titolo").eq("id", ref).limit(1).execute()
    data = (row.data or [{}])[0]
    val = data.get("foto")
    if isinstance(val, list):
        for u in val:
            abs_u = resolve_image_url(str(u), supabase_url)
            if abs_u and abs_u not in out:
                out.append(abs_u)
    return out


def collect_photo_urls(
    *,
    sb: Client,
    supabase_url: str,
    fonte: str,
    ref: str | None,
    link_pagina: str | None,
) -> list[str]:
    urls: list[str] = []
    fonte = (fonte or "").strip().lower()

    page = _valid_page_url(link_pagina)
    if page:
        og = fetch_og_image(page)
        if og and og not in urls:
            urls.append(og)

    if fonte in ("reel_manuale", "notizia_esterna", "sito") and ref:
        for try_fonte in ("blog", "immobile"):
            extra = collect_photo_urls(
                sb=sb,
                supabase_url=supabase_url,
                fonte=try_fonte,
                ref=ref,
                link_pagina=None,
            )
            for u in extra:
                if u not in urls:
                    urls.append(u)
            if urls:
                break

    if fonte == "immobile" and ref:
        for u in _immobile_photos(sb, ref, supabase_url):
            if u not in urls:
                urls.append(u)

    elif fonte == "blog" and ref:
        row = sb.table("blog").select("*").eq("id", ref).limit(1).execute()
        data = (row.data or [{}])[0]
        cov = resolve_image_url(str(data.get("immagine_copertina") or ""), supabase_url)
        if cov:
            urls.append(cov)
        slug = data.get("slug") or data.get("url_statico") or ""
        if slug:
            page = f"{BASE_SITE}/blog-articolo?s={slug}"
            og = fetch_og_image(page)
            if og and og not in urls:
                urls.append(og)

    elif fonte == "landing" and ref:
        row = sb.table("landing_pages").select("*").eq("id", ref).limit(1).execute()
        data = (row.data or [{}])[0]
        path = data.get("url") or f"/{data.get('slug', '')}"
        if not str(path).startswith("http"):
            path = BASE_SITE.rstrip("/") + (
                path if str(path).startswith("/") else "/" + str(path)
            )
        og = fetch_og_image(path)
        if og:
            urls.append(og)

    if not urls and ref:
        for u in _immobile_photos(sb, ref, supabase_url):
            if u not in urls:
                urls.append(u)

    return urls[:MAX_IMAGES]


def download_images(urls: list[str], dest: Path) -> list[Path]:
    dest.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i, url in enumerate(urls):
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=40)
            r.raise_for_status()
            ext = ".jpg"
            ct = (r.headers.get("content-type") or "").lower()
            if "png" in ct or url.lower().endswith(".png"):
                ext = ".png"
            elif "webp" in ct or url.lower().endswith(".webp"):
                ext = ".webp"
            fp = dest / f"slide_{i:02d}{ext}"
            fp.write_bytes(r.content)
            paths.append(fp)
        except requests.RequestException as e:
            print(f"Skip immagine {url[:60]}: {e}", file=sys.stderr)
    return paths


def font_file() -> str | None:
    for p in (
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if Path(p).is_file():
            return p.replace("\\", "/").replace(":", "\\:")
    return None


def ffmpeg_safe_text(text: str, max_len: int = 48) -> str:
    t = (text or "").replace("\n", " ")
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[\\':;%]", " ", t)
    return t.strip()[:max_len] or "Righetto Immobiliare"


def build_mp4(
    slides: list[Path],
    output: Path,
    *,
    title: str,
    subtitle: str,
    ffmpeg: str,
) -> None:
    if not slides:
        raise RuntimeError("Nessuna immagine scaricata per il reel")

    n = len(slides)
    d_frames = SEC_PER_SLIDE * 30
    inputs: list[str] = []
    for p in slides:
        inputs.extend(["-loop", "1", "-t", str(SEC_PER_SLIDE), "-i", str(p)])

    parts: list[str] = []
    concat_in = ""
    ff = font_file()
    safe_title = ffmpeg_safe_text(title, 42)
    safe_sub = ffmpeg_safe_text(subtitle, 36)

    for i in range(n):
        chain = (
            f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color={BG},"
            f"zoompan=z='min(zoom+0.0012,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={d_frames}:s=1080x1920:fps=30"
        )
        if i == 0 and ff:
            chain += (
                f",drawtext=fontfile='{ff}':text='{safe_title}':"
                f"fontcolor=white:fontsize=46:borderw=2:bordercolor=0x1a2744:"
                f"x=(w-text_w)/2:y=h-320,"
                f"drawtext=fontfile='{ff}':text='{safe_sub}':"
                f"fontcolor=0xCEE08F:fontsize=32:borderw=1:bordercolor=0x1a2744:"
                f"x=(w-text_w)/2:y=h-250"
            )
        chain += f"[v{i}]"
        parts.append(chain)
        concat_in += f"[v{i}]"

    parts.append(f"{concat_in}concat=n={n}:v=1:a=0[vout]")
    filter_cx = ";".join(parts)

    cmd = [
        ffmpeg,
        "-y",
        *inputs,
        "-filter_complex",
        filter_cx,
        "-map",
        "[vout]",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        "-movflags",
        "+faststart",
        str(output),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg errore:\n{proc.stderr[-1200:]}")


def upload_mp4(sb: Client, local_path: Path, slug: str) -> str:
    supabase_url = req_env("SUPABASE_URL").rstrip("/")
    bucket = os.environ.get("REEL_STORAGE_BUCKET", "foto-immobili").strip()
    storage_path = f"reels/{slug}.mp4"
    data = local_path.read_bytes()
    sb.storage.from_(bucket).upload(
        storage_path,
        data,
        file_options={"content-type": "video/mp4", "upsert": "true"},
    )
    return f"{supabase_url}/storage/v1/object/public/{bucket}/{storage_path}"


def expand_spintax(text: str) -> str:
    out = text or ""
    prev = None
    while prev != out:
        prev = out
        out = re.sub(
            r"\{([^{}]+)\}",
            lambda m: (m.group(1).split("|")[0].strip() if m.group(1) else ""),
            out,
        )
    return out


def process_bozza(sb: Client, bozza: dict[str, Any], *, ffmpeg: str) -> str | None:
    if (bozza.get("tipo_canale") or "") != "instagram_reel":
        return None
    if (bozza.get("media_direct_url") or "").strip().endswith(".mp4"):
        print(f"Skip {bozza.get('id')}: MP4 gia presente")
        return bozza.get("media_direct_url")

    supabase_url = req_env("SUPABASE_URL")
    urls = collect_photo_urls(
        sb=sb,
        supabase_url=supabase_url,
        fonte=str(bozza.get("fonte") or ""),
        ref=bozza.get("riferimento_id"),
        link_pagina=bozza.get("link_pagina"),
    )
    if not urls:
        print(f"Skip {bozza.get('id')}: nessuna immagine", file=sys.stderr)
        return None

    title = expand_spintax(bozza.get("titolo") or "Righetto Immobiliare")
    subtitle = "Consulenza gratuita · Padova"
    stamp = datetime.now(tz=TZ).strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower())[:40].strip("-") or "reel"
    slug = f"{stamp}_{slug}"

    OUT_LOCAL.mkdir(parents=True, exist_ok=True)
    local_mp4 = OUT_LOCAL / f"{slug}.mp4"

    with tempfile.TemporaryDirectory(prefix="rig_reel_") as tmp:
        slides = download_images(urls, Path(tmp))
        if len(slides) < 1:
            return None
        build_mp4(slides, local_mp4, title=title, subtitle=subtitle, ffmpeg=ffmpeg)

    public_url = upload_mp4(sb, local_mp4, slug)
    bid = bozza.get("id")
    if bid:
        sb.table("bozze_social").update(
            {
                "media_direct_url": public_url,
                "updated_at": datetime.now(tz=TZ).isoformat(),
                "note": (bozza.get("note") or "")
                + f" | MP4 auto {datetime.now(tz=TZ).isoformat()[:16]}",
            }
        ).eq("id", bid).execute()
    print(f"OK reel: {public_url}")
    return public_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera MP4 reel da foto sito")
    parser.add_argument("--pending", action="store_true", help="Tutte le bozze reel senza mp4")
    parser.add_argument("--bozza-id", type=str, help="UUID bozza singola")
    args = parser.parse_args()
    load_env()
    ffmpeg = find_ffmpeg()
    sb = sb_client()

    if args.bozza_id:
        res = sb.table("bozze_social").select("*").eq("id", args.bozza_id).limit(1).execute()
        rows = res.data or []
    elif args.pending:
        res = (
            sb.table("bozze_social")
            .select("*")
            .eq("stato", "bozza")
            .eq("tipo_canale", "instagram_reel")
            .execute()
        )
        rows = res.data or []
    else:
        parser.print_help()
        return 1

    if not rows:
        print("Nessuna bozza reel da elaborare.")
        return 0

    ok = 0
    for row in rows:
        try:
            if process_bozza(sb, row, ffmpeg=ffmpeg):
                ok += 1
        except Exception as e:
            print(f"Errore bozza {row.get('id')}: {e}", file=sys.stderr)
    print(f"Completati {ok}/{len(rows)} reel.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
