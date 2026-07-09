"""
Reel 9:16 (1080x1920, 10 s) — blog RTC affitto studenti Padova.
Usa le 3 PNG verticali in assets/blog-rtc-studenti-padova-2026/ + musica calm.

Uso:
  python genera_reel_rtc_studenti.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets" / "blog-rtc-studenti-padova-2026"
OUT_DIR = ROOT / "generated-reels"
MUSIC_CALM = ROOT / "assets" / "reel_music_calm.mp3"
MUSIC_FALLBACK = ROOT / "assets" / "reel_music.mp3"
BG = "0x1a2744"
FPS = 30
TOTAL_SEC = 10.0
SLIDE_SEC = [3.4, 3.3, 3.3]
SLIDES = (
    "ig-rtc-studenti-padova-cover.png",
    "ig-rtc-studenti-padova-slide2.png",
    "ig-rtc-studenti-padova-slide3-cta.png",
)


def find_ffmpeg() -> str:
    from genera_reel import find_ffmpeg as _ff

    return _ff()


def build_video(slides: list[Path], output: Path, ffmpeg: str) -> None:
    inputs: list[str] = []
    parts: list[str] = []
    concat_in = ""

    for i, (path, dur) in enumerate(zip(slides, SLIDE_SEC)):
        inputs.extend(["-loop", "1", "-t", str(dur), "-i", str(path)])
        parts.append(
            f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color={BG},"
            f"setsar=1,fps={FPS},trim=duration={dur},setpts=PTS-STARTPTS[v{i}]"
        )
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
        "-t",
        str(TOTAL_SEC),
        "-movflags",
        "+faststart",
        str(output),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[-1500:])


def add_music(video: Path, ffmpeg: str) -> Path:
    music = MUSIC_CALM if MUSIC_CALM.is_file() else MUSIC_FALLBACK
    if not music.is_file():
        return video
    out = video.with_name(video.stem + "_audio.mp4")
    fade_out = max(0.5, TOTAL_SEC - 1.5)
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video),
        "-i",
        str(music),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-af",
        f"volume=0.14,afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out}:d=1.5",
        "-shortest",
        "-t",
        str(TOTAL_SEC),
        str(out),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[musica] skip: {proc.stderr[-400:]}", file=sys.stderr)
        return video
    return out


def main() -> int:
    ffmpeg = find_ffmpeg()
    slides = [ASSETS / name for name in SLIDES]
    missing = [p for p in slides if not p.is_file()]
    if missing:
        print("Mancano immagini:", ", ".join(p.name for p in missing), file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    silent = OUT_DIR / "blog-rtc-studenti-padova-2026_silent.mp4"
    final = OUT_DIR / "blog-rtc-studenti-padova-2026.mp4"

    print("Generazione video 1080x1920 (10 s)...")
    build_video(slides, silent, ffmpeg)
    with_audio = add_music(silent, ffmpeg)
    if with_audio != silent:
        with_audio.replace(final)
        silent.unlink(missing_ok=True)
    else:
        silent.replace(final)

    print(f"OK: {final}")
    print(f"Slide: {len(slides)} x ~{sum(SLIDE_SEC)} s · musica: {music_label()}")

    reels_site = ROOT.parent / "img" / "video" / "reels"
    reels_site.mkdir(parents=True, exist_ok=True)
    site_copy = reels_site / "blog-rtc-studenti-padova-2026.mp4"
    shutil.copy2(final, site_copy)
    print(f"Copia sito: {site_copy}")
    return 0


def music_label() -> str:
    if MUSIC_CALM.is_file():
        return "reel_music_calm.mp3 (soft, professionale)"
    if MUSIC_FALLBACK.is_file():
        return "reel_music.mp3"
    return "nessuna"


if __name__ == "__main__":
    raise SystemExit(main())
