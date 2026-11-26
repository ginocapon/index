"""Lettura clienti/immobili e upload documenti (service_role)."""
from __future__ import annotations

import re
import time
from typing import Any

from supabase import create_client

from env_config import dry_run, supabase_service_key, supabase_url

LEGACY_RE = re.compile(r"(?:originale:|gestionale)\s*(\d{1,12})", re.I)


def sb():
    return create_client(supabase_url(), supabase_service_key())


def legacy_id_from_note(note: str | None) -> str | None:
    if not note:
        return None
    m = LEGACY_RE.search(note)
    return m.group(1) if m else None


def list_clienti_with_legacy(limit: int | None = None) -> list[dict[str, Any]]:
    q = sb().table("clienti").select("id,note,documenti_cliente,nome,email").order("created_at")
    if limit:
        q = q.limit(limit)
    rows = q.execute().data or []
    out = []
    for r in rows:
        lid = legacy_id_from_note(r.get("note"))
        if lid:
            r["legacy_id"] = lid
            out.append(r)
    return out


def list_immobili(limit: int | None = None) -> list[dict[str, Any]]:
    q = (
        sb()
        .table("immobili")
        .select("id,codice,documenti,planimetrie,titolo")
        .order("codice")
    )
    if limit:
        q = q.limit(limit)
    return q.execute().data or []


def _ext(name: str) -> str:
    if "." in name:
        return name.rsplit(".", 1)[-1].upper()
    return "FILE"


def _has_doc(docs: list | None, nome: str) -> bool:
    if not docs:
        return False
    nome_l = nome.lower()
    return any((d.get("nome") or "").lower() == nome_l for d in docs if isinstance(d, dict))


def upload_bytes(bucket: str, path: str, data: bytes, content_type: str) -> str:
    client = sb()
    client.storage.from_(bucket).upload(
        path,
        data,
        file_options={"content-type": content_type, "upsert": "false"},
    )
    pub = client.storage.from_(bucket).get_public_url(path)
    return pub.get("publicUrl") or pub  # type: ignore[return-value]


def append_cliente_doc(cliente_id: str, docs: list | None, nome: str, url: str, tipo: str) -> None:
    if _has_doc(docs, nome):
        return
    new_docs = list(docs or [])
    new_docs.append({"url": url, "nome": nome, "tipo": tipo})
    if dry_run():
        return
    sb().table("clienti").update({"documenti_cliente": new_docs}).eq("id", cliente_id).execute()


def append_immobile_doc(
    imm_id: str,
    field: str,
    docs: list | None,
    nome: str,
    url: str,
    tipo: str,
) -> None:
    if field not in ("documenti", "planimetrie"):
        raise ValueError(field)
    if _has_doc(docs, nome):
        return
    new_docs = list(docs or [])
    new_docs.append({"url": url, "nome": nome, "tipo": tipo})
    if dry_run():
        return
    sb().table("immobili").update({field: new_docs}).eq("id", imm_id).execute()


def store_file(bucket: str, safe_prefix: str, filename: str, data: bytes, content_type: str) -> str:
    ts = int(time.time() * 1000)
    path = f"{safe_prefix}/{ts}-{filename}".replace(" ", "_")
    if dry_run():
        return f"dry-run://{bucket}/{path}"
    return upload_bytes(bucket, path, data, content_type)
