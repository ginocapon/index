"""Lettura allegati dal pannello legacy (dyna_media get_allegati_array + cloud)."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal
from urllib.parse import urljoin

if TYPE_CHECKING:
    from playwright.sync_api import BrowserContext, Page

ItemKind = Literal["clienti", "immobili"]


@dataclass
class LegacyFile:
    file_name: str
    url_file: str
    file_type: str
    flag_planimetria: bool
    source: str  # misc | image | cloud


def _details_url(kind: ItemKind, item_id: str) -> str:
    base = "https://pannello.gestionaleimmobiliare.it"
    if kind == "clienti":
        return f"{base}/cliente_details.html?cliente_id={item_id}&flag_menu=allegati"
    return f"{base}/immobile_details.html?immobile_id={item_id}&flag_menu=allegati"


def _parse_item_files(payload: dict) -> list[LegacyFile]:
    out: list[LegacyFile] = []
    item_files = payload.get("item_files")
    if isinstance(item_files, list):
        return out
    if not isinstance(item_files, dict):
        return out
    for section in ("misc", "image"):
        block = item_files.get(section)
        if isinstance(block, dict):
            items = block.values()
        elif isinstance(block, list):
            items = block
        else:
            continue
        for row in items:
            if not isinstance(row, dict):
                continue
            name = (row.get("file_name") or "").strip()
            url = (row.get("url_file") or "").strip()
            if not name or not url:
                continue
            out.append(
                LegacyFile(
                    file_name=name,
                    url_file=url,
                    file_type=(row.get("file_type") or "").lower(),
                    flag_planimetria=bool(row.get("flag_planimetria")),
                    source="image" if section == "image" else "misc",
                )
            )
    return out


def fetch_dyna_allegati(page: Page, kind: ItemKind, item_id: str) -> list[LegacyFile]:
    captured: list[dict] = []

    def on_resp(response):
        if "get_allegati_array" not in response.url:
            return
        try:
            captured.append(response.json())
        except Exception:
            pass

    page.on("response", on_resp)
    page.goto(_details_url(kind, item_id), timeout=120_000, wait_until="domcontentloaded")
    page.wait_for_timeout(5_000)

    files: list[LegacyFile] = []
    seen: set[str] = set()
    for payload in captured:
        for f in _parse_item_files(payload):
            if f.url_file in seen:
                continue
            seen.add(f.url_file)
            files.append(f)
    return files


def fetch_cloud(ctx: BrowserContext, kind: ItemKind, item_id: str) -> list[LegacyFile]:
    module = "clienti" if kind == "clienti" else "immobili"
    url = (
        "https://pannello.gestionaleimmobiliare.it/dyna_allegati_cloud.html"
        f"?action=get&module={module}&parent_id={item_id}"
    )
    resp = ctx.request.get(url, timeout=60_000)
    if not resp.ok:
        return []
    try:
        data = resp.json()
    except Exception:
        body = resp.text().strip()
        if body.startswith("["):
            data = json.loads(body)
        else:
            return []
    out: list[LegacyFile] = []
    if not isinstance(data, list):
        return out
    for row in data:
        if not isinstance(row, dict):
            continue
        name = (row.get("name") or row.get("file_name") or "").strip()
        url_f = (row.get("url") or row.get("url_file") or "").strip()
        if not url_f:
            continue
        if not name:
            name = url_f.rsplit("/", 1)[-1]
        url_f = urljoin("https://pannello.gestionaleimmobiliare.it/", url_f)
        out.append(
            LegacyFile(
                file_name=name,
                url_file=url_f,
                file_type=name.rsplit(".", 1)[-1].lower() if "." in name else "",
                flag_planimetria=False,
                source="cloud",
            )
        )
    return out


def fetch_all(ctx: BrowserContext, kind: ItemKind, item_id: str) -> list[LegacyFile]:
    page = ctx.new_page()
    try:
        dyna = fetch_dyna_allegati(page, kind, item_id)
    finally:
        page.close()
    cloud = fetch_cloud(ctx, kind, item_id)
    seen: set[str] = set()
    merged: list[LegacyFile] = []
    for f in dyna + cloud:
        if f.url_file in seen:
            continue
        seen.add(f.url_file)
        merged.append(f)
    return merged


def list_client_ids_from_page(html: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"cliente_details\.html\?cliente_id=(\d+)", html)))


def list_immobile_ids_from_page(html: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"immobile_details\.html\?immobile_id=(\d+)", html)))
