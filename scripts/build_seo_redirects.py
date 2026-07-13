# -*- coding: utf-8 -*-
"""Genera 404.html, js/redirects-404.js e stub HTML per URL legacy (GSC 404/5xx)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.righettoimmobiliare.it"

# Path (senza dominio) → destinazione path
MANUAL: dict[str, str] = {
    "/": "/",
    "/home": "/",
    "/home.html": "/",
    "/index.html": "/",
    "/index.php": "/",
    "/agenzia": "/agenzia-immobiliare-padova",
    "/agenzia.html": "/agenzia-immobiliare-padova",
    "/righetto": "/",
    "/righetto.html": "/",
    "/immobili.php": "/immobili",
    "/immobili.html": "/immobili",
    "/immobile.html": "/immobile",
    "/privacy.html": "/privacy-policy",
    "/privacy-policy.html": "/privacy-policy",
    "/cookie-policy.html": "/cookie-policy",
    "/chi-siamo/": "/chi-siamo",
    "/contatti/": "/contatti",
    "/servizi/": "/servizi",
    "/blog/": "/blog",
    "/immobili/": "/immobili",
    "/api/send-mail.php": "/contatti",
    "/api/": "/contatti",
    "/wp-admin": "/",
    "/wp-admin/": "/",
    "/wp-login.php": "/",
    # Wix / vecchi path comuni
    "/chi-siamo.html": "/chi-siamo",
    "/contatti.html": "/contatti",
    "/servizi.html": "/servizi",
    "/blog.html": "/blog",
    "/blog-bonus-edilizi-2024-incentivi-casa-padova": "/blog-bonus-edilizi-2026-incentivi-casa-padova",
    "/blog-affitti-canoni-fimaa-q1-2024-padova": "/blog-affitti-canoni-fimaa-q1-2026-padova",
    "/blog-vigonza-rubano-comprare-casa-cintura-2024": "/blog-vigonza-rubano-comprare-casa-cintura-2026",
    "/blog-piano-casa-decreto-salva-casa-padova": "/blog-piano-casa-decreto-66-2026-padova",
    "/landing-demo-albergo-statale-padova-vicenza": "/landing-demo-loft-adiacenti-padova-vicenza",
    "/landing-demo-hotel-mini-loft-padova-vicenza": "/landing-demo-loft-adiacenti-padova-vicenza",
    "/landing-demo-hotel-venice-grisignano": "/landing-demo-loft-adiacenti-padova-vicenza",
}

BLOG_ARTICOLO_REDIRECTS = {
    "comprare-casa-o-affittare-la-verita-dei-numeri-dopo-30-anni-padova": "blog-comprare-affittare-padova",
    "ca-marcello-mestre-hub-turistico-da-70-milioni-padova": "blog-ca-marcello-mestre",
    "righetto-immobiliare-dal-2000-storia-zone-e-ultime-acquisizioni-padova": "blog-righetto-storia-territorio-acquisizioni-2026",
    "blog-righetto-storia-territorio-acquisizioni-2026": "blog-righetto-storia-territorio-acquisizioni-2026",
    "bonus-edilizi-2026-detrazioni-50-e-ecobonus-per-padova": "blog-bonus-edilizi-2026-incentivi-casa-padova",
    "blog-bonus-edilizi-2026-incentivi-casa-padova": "blog-bonus-edilizi-2026-incentivi-casa-padova",
    "umidita-negli-scantinati-a-padova-cause-tecniche-prove-scientifiche-e-soluzioni-padova": "blog",
    "servizi-immobiliari-2026-crescita-digitale-e-nuove-opportunita-righetto-immobili-padova": "blog",
}

REDIRECT_STUB_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>Reindirizzamento — Righetto Immobiliare</title>
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0;url={target}">
<script>location.replace("{target}");</script>
</head>
<body>
<p>Pagina spostata. <a href="{target}">Continua su Righetto Immobiliare</a>.</p>
</body>
</html>
"""

HTACCESS_MARKER_START = "# ── SEO redirects (build_seo_redirects.py) ──"
HTACCESS_MARKER_END = "# ── Fine SEO redirects ──"


def collect_blog_static() -> dict[str, str]:
    blog = (ROOT / "blog.html").read_text(encoding="utf-8", errors="replace")
    out: dict[str, str] = {}
    for m in re.finditer(r'"url_statico":\s*"([^"]+)"', blog):
        slug = m.group(1).strip()
        if not slug or slug == "blog-articolo":
            continue
        out[f"/blog-articolo?s={slug}"] = f"/{slug}"
        out[f"/blog-articolo.html?s={slug}"] = f"/{slug}"
    for src, dst in BLOG_ARTICOLO_REDIRECTS.items():
        out[f"/blog-articolo?s={src}"] = f"/{dst}"
    return out


def collect_share_legacy() -> dict[str, str]:
    """Share page senza file: redirect a immobili o scheda attiva."""
    out: dict[str, str] = {}
    og_path = ROOT / "data" / "og-immobili.json"
    if not og_path.is_file():
        return out
    data = json.loads(og_path.read_text(encoding="utf-8"))
    on_disk = {p.stem for p in ROOT.glob("share-immobile-*.html")}
    for row in data.get("bySlug", {}).values():
        share_file = (row.get("share_file") or "").replace(".html", "")
        if not share_file:
            continue
        app = row.get("app_url", "")
        target = "/immobili"
        if "?s=" in app:
            target = "/immobile" + app.split("righettoimmobiliare.it", 1)[-1].replace(
                "https://www.righettoimmobiliare.it", ""
            ).replace("https://righettoimmobiliare.it", "")
        path = "/" + share_file
        if share_file not in on_disk:
            out[path] = target
    return out


def merge_redirects() -> dict[str, str]:
    merged = dict(MANUAL)
    merged.update(collect_blog_static())
    merged.update(collect_share_legacy())
    # Normalizza: no doppioni, destinazioni senza dominio
    clean: dict[str, str] = {}
    for src, dst in merged.items():
        src = src if src.startswith("/") else "/" + src
        dst = dst if dst.startswith("/") else "/" + dst
        if src == dst:
            continue
        clean[src] = dst
    return dict(sorted(clean.items()))


def abs_url(path: str) -> str:
    return SITE + (path if path.startswith("/") else "/" + path)


def write_redirects_js(redirects: dict[str, str]) -> None:
    js_path = ROOT / "js" / "redirects-404.js"
    payload = json.dumps(redirects, ensure_ascii=False, separators=(",", ":"))
    js_path.write_text(
        "/* Auto-generato da scripts/build_seo_redirects.py — non editare a mano */\n"
        f"window.RIGHETTO_REDIRECTS = {payload};\n",
        encoding="utf-8",
    )
    print(f"js/redirects-404.js: {len(redirects)} regole")


def write_404_html() -> None:
    html = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>Pagina non trovata — Righetto Immobiliare</title>
<link rel="stylesheet" href="css/fonts.css?v=3">
<script src="js/redirects-404.js?v=1"></script>
<script>
(function () {
  var map = window.RIGHETTO_REDIRECTS || {};
  var path = location.pathname.replace(/\\/+$/, '') || '/';
  var qs = location.search || '';
  var key = path + qs;
  var target = map[key] || map[path];
  if (!target && path === '/blog-articolo' && qs.indexOf('s=') > -1) {
    var slug = new URLSearchParams(qs).get('s');
    if (slug) {
      target = map['/blog-articolo?s=' + slug] || (slug.indexOf('blog-') === 0 ? '/' + slug : '/blog');
    }
  }
  if (!target && path.indexOf('/share-immobile-') === 0) target = '/immobili';
  if (!target && path === '/immobile' && qs) target = '/immobili';
  if (target) {
    location.replace(target);
    return;
  }
})();
</script>
<style>
  body{font-family:system-ui,sans-serif;background:#f0ece6;color:#152435;margin:0;padding:2rem 1.25rem;text-align:center}
  h1{font-size:1.35rem;margin:0 0 .5rem}
  p{color:#6b7a8d;line-height:1.6;max-width:28rem;margin:0 auto 1.25rem}
  a{color:#2c4a6e;font-weight:600}
</style>
</head>
<body>
<h1>Pagina non trovata</h1>
<p>L'indirizzo potrebbe essere cambiato o l'immobile non è più disponibile.</p>
<p><a href="/">Home</a> · <a href="/immobili">Immobili in vendita e affitto</a> · <a href="/contatti">Contatti</a></p>
</body>
</html>
"""
    (ROOT / "404.html").write_text(html, encoding="utf-8")
    print("404.html aggiornato")


def existing_page_paths() -> set[str]:
    paths: set[str] = set()
    for p in ROOT.glob("*.html"):
        paths.add("/" + p.stem)
        paths.add("/" + p.name)
    for p in ROOT.glob("*/*.html"):
        if p.parent.name in (".git", "node_modules", "scripts", "TEST-SKILL"):
            continue
        paths.add("/" + p.parent.name)
        paths.add("/" + p.parent.name + "/")
    return paths


def write_stub_files(redirects: dict[str, str]) -> list[str]:
    """Nessuno stub HTML in root: redirect via 404.html + js/redirects-404.js (audit compliance pulito)."""
    return []


def write_redirects_json(redirects: dict[str, str]) -> None:
    data = {
        "site": SITE,
        "generated_by": "scripts/build_seo_redirects.py",
        "count": len(redirects),
        "redirects": redirects,
    }
    (ROOT / "data" / "redirects-301.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def patch_htaccess(redirects: dict[str, str]) -> None:
    ht = ROOT / ".htaccess"
    text = ht.read_text(encoding="utf-8")
    if HTACCESS_MARKER_START in text:
        text = text.split(HTACCESS_MARKER_START)[0].rstrip() + "\n"
    rules = [
        "",
        HTACCESS_MARKER_START,
        "<IfModule mod_rewrite.c>",
        "  RewriteEngine On",
        "  # Trailing slash → senza slash (pagine .html)",
        "  RewriteCond %{REQUEST_FILENAME} !-d",
        "  RewriteRule ^(.+)/$ /$1 [R=301,L]",
    ]
    for src, dst in redirects.items():
        if "?" in src:
            continue
        pat = src.lstrip("/").replace(".", r"\.")
        if not pat:
            continue
        rules.append(f"  RewriteRule ^{pat}$ {dst} [R=301,L]")
    rules.extend(["</IfModule>", HTACCESS_MARKER_END, ""])
    ht.write_text(text + "\n".join(rules), encoding="utf-8")
    print(".htaccess: regole redirect aggiunte")


def write_trailing_slash_indexes(redirects: dict[str, str]) -> list[str]:
    skip_folders = {"wp-admin", "api"}
    created: list[str] = []
    for src, dst in redirects.items():
        if not src.endswith("/") or src == "/":
            continue
        folder = src.strip("/")
        if folder in skip_folders:
            continue
        idx = ROOT / folder / "index.html"
        if idx.is_file():
            continue
        idx.parent.mkdir(parents=True, exist_ok=True)
        target = abs_url(dst)
        idx.write_text(
            REDIRECT_STUB_TEMPLATE.format(canonical=target, target=target),
            encoding="utf-8",
        )
        created.append(str(idx.relative_to(ROOT)))
    return created


def main() -> None:
    redirects = merge_redirects()
    write_redirects_json(redirects)
    write_redirects_js(redirects)
    write_404_html()
    stubs = write_stub_files(redirects)
    indexes = write_trailing_slash_indexes(redirects)
    patch_htaccess(redirects)
    print(f"Stub creati: {len(stubs)}")
    for s in stubs:
        print(f"  + {s}")
    print(f"Index trailing-slash: {len(indexes)}")
    for s in indexes:
        print(f"  + {s}")


if __name__ == "__main__":
    main()
