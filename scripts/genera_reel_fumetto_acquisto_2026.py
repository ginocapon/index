#!/usr/bin/env python3
"""Reel 30s — percorso acquisto casa fumetto (4 vignette, transizioni FFmpeg)."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(
    r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets"
)
OUT_REELS = ROOT / "img" / "video" / "reels"
OUT_SOCIAL = ROOT / "righetto_social" / "generated-reels"
SLUG = "blog-percorso-acquisto-casa-padova-fumetto-2026-reel"
BG = "0x152435"
CLIP_SEC = 8.0
FADE_SEC = 0.85
FPS = 30
TARGET_W, TARGET_H = 1080, 1920

# Episodi 1 → 4 (ordine narrativo)
SOURCE_NAMES = [
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_Truffa_immobiliare__prezzi_diversi__stessa_casa-8661793f-8a39-4959-ad3c-dab49b7cdeaf.jpg",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_Consulenza_immobiliare_in_citt__italiana-cf0352bf-f40f-41bb-bd56-869df5e39a52.jpg",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_Proposta_d_acquisto_accettata__1_-75551f2d-b36c-473c-a770-18a957dfa17d.jpg",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_Finalmente__casa_nostra__1_-2f304708-e951-45b5-9b81-62e8fba4e679.jpg",
]
TRANSITIONS = ("fade", "slideleft", "wiperight", "circleopen")


def find_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    for c in (
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
    ):
        if Path(c).is_file():
            return c
    raise SystemExit("FFmpeg non trovato.")


def slide_filter(idx: int) -> str:
    z = 1.0 + idx * 0.015
    return (
        f"[{idx}:v]scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=decrease,"
        f"pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2:color={BG},"
        f"setsar=1,fps={FPS},format=yuv420p,"
        f"zoompan=z='min(zoom+0.0012,{z})':d={int(CLIP_SEC * FPS)}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={TARGET_W}x{TARGET_H}:fps={FPS},"
        f"trim=duration={CLIP_SEC},setpts=PTS-STARTPTS[v{idx}]"
    )


def build_xfade_chain(n: int) -> tuple[str, str]:
    parts: list[str] = []
    for i in range(n):
        parts.append(slide_filter(i))
    label = "v0"
    for i in range(1, n):
        prev = label
        label = f"vx{i}"
        off = i * CLIP_SEC - i * FADE_SEC
        tr = TRANSITIONS[(i - 1) % len(TRANSITIONS)]
        parts.append(
            f"[{prev}][v{i}]xfade=transition={tr}:duration={FADE_SEC}:offset={off:.3f}[{label}]"
        )
    return ";".join(parts), label


def main() -> None:
    ffmpeg = find_ffmpeg()
    tmp = ROOT / "documenti" / "_tmp_reel_fumetto_frames"
    tmp.mkdir(parents=True, exist_ok=True)
    slides: list[Path] = []
    for i, name in enumerate(SOURCE_NAMES):
        src = ASSETS / name
        if not src.is_file():
            print(f"Manca asset: {src}", file=sys.stderr)
            sys.exit(1)
        dest = tmp / f"ep{i + 1:02d}.jpg"
        shutil.copy2(src, dest)
        slides.append(dest)

    filter_cx, out_label = build_xfade_chain(len(slides))
    OUT_REELS.mkdir(parents=True, exist_ok=True)
    OUT_SOCIAL.mkdir(parents=True, exist_ok=True)
    out_path = OUT_REELS / f"{SLUG}.mp4"

    cmd = [ffmpeg, "-y"]
    for p in slides:
        cmd.extend(["-loop", "1", "-t", str(CLIP_SEC), "-i", str(p)])
    cmd.extend(
        [
            "-filter_complex",
            filter_cx,
            "-map",
            f"[{out_label}]",
            "-t",
            "30",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(FPS),
            "-crf",
            "20",
            "-movflags",
            "+faststart",
            str(out_path),
        ]
    )
    print("Generazione reel…")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-2000:], file=sys.stderr)
        sys.exit(proc.returncode)

    social_copy = OUT_SOCIAL / f"{SLUG}.mp4"
    shutil.copy2(out_path, social_copy)
    print(f"OK: {out_path}")
    print(f"Copia: {social_copy}")
    print(f"URL: https://righettoimmobiliare.it/img/video/reels/{SLUG}.mp4")


if __name__ == "__main__":
    main()
