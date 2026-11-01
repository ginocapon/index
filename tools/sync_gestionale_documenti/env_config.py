"""Carica secret da variabili ambiente (Environment secrets o .env locale non committato)."""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_config() -> dict:
    for name in ("config.local.json", "config.json"):
        p = ROOT / name
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    example = ROOT / "config.example.json"
    if example.is_file():
        return json.loads(example.read_text(encoding="utf-8"))
    raise SystemExit("Manca config.local.json (copia da config.example.json)")


def supabase_url() -> str:
    url = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    if not url:
        raise SystemExit("Imposta SUPABASE_URL nei secret ambiente")
    return url


def supabase_service_key() -> str:
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not key:
        raise SystemExit("Imposta SUPABASE_SERVICE_ROLE_KEY nei secret ambiente")
    return key


def gestionale_base_url(cfg: dict) -> str:
    env_name = cfg.get("base_url_env") or "GESTIONALE_BASE_URL"
    return (
        os.environ.get(env_name, "").strip()
        or cfg.get("base_url")
        or "https://pannello.gestionaleimmobiliare.it"
    ).rstrip("/")


def dry_run() -> bool:
    return os.environ.get("SYNC_DRY_RUN", "1").strip().lower() in ("1", "true", "yes")


def storage_state() -> dict | None:
    raw = os.environ.get("GESTIONALE_STORAGE_STATE", "").strip()
    if not raw:
        path = os.environ.get("GESTIONALE_STORAGE_STATE_PATH", "").strip()
        if path and Path(path).is_file():
            raw = Path(path).read_text(encoding="utf-8")
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit("GESTIONALE_STORAGE_STATE non è JSON valido") from e


def has_password_login() -> bool:
    return bool(
        os.environ.get("GESTIONALE_USER", "").strip()
        and os.environ.get("GESTIONALE_PASSWORD", "").strip()
    )
