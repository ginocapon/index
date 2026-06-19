# -*- coding: utf-8 -*-
"""
Reel 9:16 (1080x1920) — intro Righetto + slideshow foto portale acquisizioni giugno 2026.
Richiede FFmpeg. Opzionale .env in righetto_social/ per foto multiple da Supabase.

Uso:
  python genera_reel_portale_acquisizioni.py
  python genera_reel_portale_acquisizioni.py --codice LP0285-V
  python genera_reel_portale_acquisizioni.py --tour
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
DATA_JSON = REPO / "scripts" / "acquisizioni_giugno16_data.json"
OUT_DIR = ROOT / "generated-reels"
MUSIC = ROOT / "assets" / "reel_music.mp3"
MUSIC_CALM = ROOT / "assets" / "reel_music_calm.mp3"
INTRO_IMG = REPO / "img" / "team" / "righetto-titolari-consulenza-2026.png"
OUTRO_IMG = REPO / "img" / "team" / "righetto-ufficio-sede-2026.png"
UA = "Mozilla/5.0 (compatible; RighettoReelGen/2.0)"
BG = "0x152435"
ORO = "0xFF6B35"
SEC_INTRO = 5
SEC_OUTRO = 4
SEC_PROP = 3.0
MAX_SEC_DEFAULT = 0
FOTO_PER_PROP = 3
TIMING: dict[str, float] = {}
FPS = 30
TZ = ZoneInfo("Europe/Rome")

RES_ORDER = ["LP0285-V", "LP0286", "LA0317", "LP0283", "LP0281"]
COM_ORDER = ["UFF2105a", "CAP1609a", "uff2189a"]


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def find_ffmpeg() -> str:
    from genera_reel import find_ffmpeg as _ff

    return _ff()


def font_file() -> str | None:
    from genera_reel import font_file as _f

    return _f()


def safe_txt(text: str, max_len: int = 44) -> str:
    t = (text or "").replace("\n", " ")
    t = t.encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[\\':;%]", " ", t)
    return t.strip()[:max_len] or "Righetto Immobiliare"


def fmt_price(p: dict) -> str:
    prezzo = p.get("prezzo")
    op = (p.get("tipo_operazione") or "").lower()
    if prezzo is None:
        return "Su richiesta"
    if "affitto" in op or (isinstance(prezzo, (int, float)) and prezzo < 5000):
        return f"EUR {int(prezzo):,}".replace(",", ".") + "/mese"
    return f"EUR {int(prezzo):,}".replace(",", ".")


def load_catalog() -> dict[str, dict]:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for p in data.get("res", []) + data.get("com", []):
        c = (p.get("codice") or "").strip()
        if c:
            out[c] = p
    return out


def fetch_foto_urls(codice: str, fallback: str, limit: int = 3) -> list[str]:
    urls: list[str] = []
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if url and key:
        try:
            from supabase import create_client

            sb = create_client(url, key)
            row = (
                sb.table("immobili")
                .select("foto,foto_urls")
                .eq("codice", codice)
                .limit(1)
                .execute()
            )
            d = (row.data or [{}])[0]
            for src in (d.get("foto"), d.get("foto_urls")):
                if isinstance(src, list):
                    for u in src:
                        u = str(u).strip()
                        if not u.startswith("http"):
                            u = f"{url.rstrip('/')}/storage/v1/object/public/{u.lstrip('/')}"
                        if u and u not in urls:
                            urls.append(u)
        except Exception as e:
            print(f"[warn] Supabase {codice}: {e}", file=sys.stderr)
    if fallback and fallback not in urls:
        urls.insert(0, fallback)
    return urls[:limit]


def download_file(url: str, dest: Path, name: str) -> Path | None:
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=45)
        r.raise_for_status()
        ext = ".jpg"
        ct = (r.headers.get("content-type") or "").lower()
        if "png" in ct or url.lower().endswith(".png"):
            ext = ".png"
        elif "webp" in ct or url.lower().endswith(".webp"):
            ext = ".webp"
        fp = dest / f"{name}{ext}"
        fp.write_bytes(r.content)
        return fp
    except requests.RequestException as e:
        print(f"Skip {url[:70]}: {e}", file=sys.stderr)
        return None


def copy_local(src: Path, dest: Path, name: str) -> Path | None:
    if not src.is_file():
        return None
    ext = src.suffix.lower() or ".png"
    fp = dest / f"{name}{ext}"
    fp.write_bytes(src.read_bytes())
    return fp


class Slide:
    def __init__(self, path: Path, line1: str, line2: str, line3: str = ""):
        self.path = path
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3


def collect_slides(
    catalog: dict[str, dict],
    codes: list[str],
    tmp: Path,
    *,
    foto_limit: int = FOTO_PER_PROP,
) -> list[Slide]:
    slides: list[Slide] = []

    intro = copy_local(INTRO_IMG, tmp, "intro") or copy_local(OUTRO_IMG, tmp, "intro")
    if intro:
        slides.append(
            Slide(
                intro,
                "Righetto Immobiliare",
                "Dal 2000 - Padova e provincia",
                "350+ immobili - 101 comuni",
            )
        )

    for cod in codes:
        p = catalog.get(cod)
        if not p:
            continue
        fotos = fetch_foto_urls(cod, p.get("foto0") or "", limit=foto_limit)
        comune = p.get("comune") or "Padova"
        tit = p.get("titolo") or cod
        l1 = f"{cod} - {comune}"
        l2 = fmt_price(p)
        mq = p.get("superficie")
        l3 = f"{mq} mq" if mq else (p.get("tipologia") or "")
        for i, url in enumerate(fotos):
            fp = download_file(url, tmp, f"{cod}_{i}")
            if fp:
                slides.append(Slide(fp, l1, l2 if i == 0 else tit[:40], l3 if i == 0 else ""))

    outro = copy_local(OUTRO_IMG, tmp, "outro") or intro
    if outro:
        slides.append(
            Slide(
                outro,
                "Scopri tutte le schede",
                "righettoimmobiliare.it",
                "Tel. 049 88 43 484",
            )
        )
    return slides


def plan_timing(slides: list[Slide], max_sec: float) -> dict[str, float]:
    """Calcola durate intro/outro/prop entro max_sec totali."""
    if max_sec <= 0 or len(slides) < 2:
        return {"intro": SEC_INTRO, "outro": SEC_OUTRO, "prop": SEC_PROP}
    n_prop = max(0, len(slides) - 2)
    intro = min(3.0, max_sec * 0.12)
    outro = min(2.5, max_sec * 0.1)
    budget = max_sec - intro - outro
    prop = budget / n_prop if n_prop else 2.0
    prop = max(1.8, min(prop, 4.0))
    total = intro + outro + n_prop * prop
    if total > max_sec:
        prop = (max_sec - intro - outro) / n_prop
    return {"intro": round(intro, 2), "outro": round(outro, 2), "prop": round(prop, 2)}


def slide_duration(slide: Slide, idx: int, total: int) -> float:
    t = TIMING or {"intro": SEC_INTRO, "outro": SEC_OUTRO, "prop": SEC_PROP}
    if idx == 0:
        return t["intro"]
    if idx == total - 1:
        return t["outro"]
    return t["prop"]


def build_reel(slides: list[Slide], output: Path, ffmpeg: str) -> None:
    if len(slides) < 2:
        raise RuntimeError("Slide insufficienti per il reel")

    ff = font_file()
    inputs: list[str] = []
    parts: list[str] = []
    concat_in = ""

    for i, sl in enumerate(slides):
        dur = slide_duration(sl, i, len(slides))
        inputs.extend(["-loop", "1", "-t", str(dur), "-i", str(sl.path)])
        chain = (
            f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color={BG},"
            f"setsar=1,fps={FPS},trim=duration={dur},setpts=PTS-STARTPTS"
        )
        if ff:
            l1, l2, l3 = safe_txt(sl.line1, 38), safe_txt(sl.line2, 42), safe_txt(sl.line3, 36)
            # barra inferiore
            chain += (
                f",drawbox=x=0:y=h-280:w=iw:h=280:color={BG}@0.72:t=fill"
            )
            chain += (
                f",drawtext=fontfile='{ff}':text='{l1}':"
                f"fontcolor=white:fontsize=40:borderw=2:bordercolor={BG}:"
                f"x=(w-text_w)/2:y=h-250"
            )
            chain += (
                f",drawtext=fontfile='{ff}':text='{l2}':"
                f"fontcolor={ORO}:fontsize=34:borderw=1:bordercolor={BG}:"
                f"x=(w-text_w)/2:y=h-195"
            )
            if l3:
                chain += (
                    f",drawtext=fontfile='{ff}':text='{l3}':"
                    f"fontcolor=0xCEE08F:fontsize=28:borderw=1:bordercolor={BG}:"
                    f"x=(w-text_w)/2:y=h-150"
                )
            # watermark alto
            chain += (
                f",drawtext=fontfile='{ff}':text='RIGHETTO IMMOBILIARE':"
                f"fontcolor=white@0.85:fontsize=26:borderw=1:bordercolor={BG}:"
                f"x=40:y=48"
            )
        chain += f"[v{i}]"
        parts.append(chain)
        concat_in += f"[v{i}]"

    parts.append(f"{concat_in}concat=n={len(slides)}:v=1:a=0[vout]")
    cmd = [
        ffmpeg,
        "-y",
        *inputs,
        "-filter_complex",
        ";".join(parts),
        "-map",
        "[vout]",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-r",
        str(FPS),
        "-movflags",
        "+faststart",
        str(output),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-1500:])


def ensure_calm_music(ffmpeg: str) -> Path:
    """Crea traccia soft da reel_music.mp3 (lowpass + volume basso + fade)."""
    if MUSIC_CALM.is_file() and MUSIC_CALM.stat().st_mtime >= MUSIC.stat().st_mtime:
        return MUSIC_CALM
    if not MUSIC.is_file():
        return MUSIC
    MUSIC_CALM.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(MUSIC),
        "-af",
        "volume=0.11,lowpass=f=2200,highpass=f=90,afade=t=in:st=0:d=2.5,afade=t=out:st=55:d=3",
        "-t",
        "60",
        str(MUSIC_CALM),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[musica calm] fallback originale: {proc.stderr[-200:]}", file=sys.stderr)
        return MUSIC
    return MUSIC_CALM


def add_music(video: Path, ffmpeg: str, max_sec: float = 0) -> Path:
    music_src = ensure_calm_music(ffmpeg)
    if not music_src.is_file():
        return video
    out = video.with_name(video.stem + "_audio.mp4")
    fade_out = max(0.5, (max_sec or 28) - 2)
    af = (
        "volume=0.16,lowpass=f=2400,highpass=f=80,"
        f"afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out:.2f}:d=1.8"
    )
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video),
        "-i",
        str(music_src),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "96k",
        "-af",
        af,
        "-shortest",
        str(out),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[musica] skip: {proc.stderr[-300:]}", file=sys.stderr)
        return video
    video.unlink(missing_ok=True)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Reel portale acquisizioni Righetto")
    parser.add_argument("--tour", action="store_true", help="Tour completo 8 immobili (default)")
    parser.add_argument("--codice", type=str, help="Singolo immobile es. LP0285-V")
    parser.add_argument("--max-sec", type=float, default=28, help="Durata massima reel (default 28 per FB)")
    parser.add_argument("--out", type=str, default="", help="Nome file output (es. portale-tour-28s.mp4)")
    args = parser.parse_args()

    global TIMING

    load_env()
    ffmpeg = find_ffmpeg()
    catalog = load_catalog()

    if args.codice:
        codes = [args.codice.strip()]
        slug = re.sub(r"[^a-z0-9]+", "-", codes[0].lower())
        label = f"reel-{slug}"
    else:
        codes = RES_ORDER + COM_ORDER
        label = "portale-acquisizioni-tour-giugno-2026"

        label = "portale-acquisizioni-tour-giugno-2026"

    foto_limit = 1 if args.max_sec > 0 else FOTO_PER_PROP

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.out:
        out = OUT_DIR / args.out
    else:
        suffix = f"-{int(args.max_sec)}s" if args.max_sec > 0 else ""
        out = OUT_DIR / f"{label}{suffix}.mp4"
    silent = out.with_name(out.stem + "_silent.mp4")

    with tempfile.TemporaryDirectory(prefix="rig_portale_reel_") as tmp:
        slides = collect_slides(catalog, codes, Path(tmp), foto_limit=foto_limit)
        TIMING = plan_timing(slides, args.max_sec)
        dur_est = TIMING["intro"] + TIMING["outro"] + max(0, len(slides) - 2) * TIMING["prop"]
        print(f"Slide: {len(slides)} · timing intro={TIMING['intro']}s prop={TIMING['prop']}s outro={TIMING['outro']}s · tot ~{dur_est:.1f}s")
        build_reel(slides, silent, ffmpeg)
        final = add_music(silent, ffmpeg, max_sec=args.max_sec or dur_est)
        if final != silent:
            silent.unlink(missing_ok=True)
        final.rename(out)

    # verifica durata reale
    probe_bin = shutil.which("ffprobe") or str(Path(ffmpeg).with_name("ffprobe.exe"))
    probe = subprocess.run(
        [probe_bin, "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(out)],
        capture_output=True,
        text=True,
    )
    real_dur = probe.stdout.strip() if probe.returncode == 0 else "?"
    print(f"OK reel: {out}")
    print(f"Durata: {real_dur}s (max {args.max_sec}) · 1080x1920 · musica tranquilla")
    return 0


if __name__ == "__main__":
    sys.exit(main())
