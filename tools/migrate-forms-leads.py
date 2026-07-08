#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Allinea form lead a skill-forms-leads.md:
- js/rig-lead-form.js + supabase/config senza defer
- Servizi: data-rig-lead-form, rimuove sendForm inline rotto
- Blog: sezione form compatta prima di </main>
- Fix ordine script su landing con handler inline prima di config defer

Uso: python tools/migrate-forms-leads.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAD_SCRIPTS = """<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="js/config.js?v=4"></script>
<script src="js/rig-lead-form.js?v=3"></script>"""

BLOG_LEAD_CSS = '<link rel="stylesheet" href="css/blog-lead-form.css?v=1">'

BLOG_FORM_TEMPLATE = """
<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Richiedi una consulenza gratuita</h2>
  <form data-rig-lead-form data-provenienza="{provenienza}" data-pagina="{provenienza}" data-msg-prefix="[Blog]" novalidate>
    <div class="bl-fields">
      <label for="bl-nome">Nome e cognome *</label>
      <input type="text" id="bl-nome" required autocomplete="name" placeholder="Mario Rossi">
      <label for="bl-tel">Telefono *</label>
      <input type="tel" id="bl-tel" required autocomplete="tel" placeholder="333 123 4567">
      <label for="bl-email">Email</label>
      <input type="email" id="bl-email" autocomplete="email" placeholder="mario@email.it">
      <label for="bl-msg">Messaggio (opzionale)</label>
      <textarea id="bl-msg" placeholder="Comune, obiettivo vendita/acquisto…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="bl-gdpr" required> Acconsento al trattamento dei dati (GDPR). <a href="privacy-policy">Privacy</a></label>
      <button type="submit">Invia richiesta</button>
    </div>
    <div class="rig-lead-success">
      <h3>Messaggio inviato!</h3>
      <p>Grazie. Ti ricontattiamo entro pochi minuti negli orari di apertura.</p>
    </div>
  </form>
</section>
"""

SERVIZIO_EXTRA = {
    "servizio-vendita.html": '{"#f-tipo":"Tipo","#f-comune":"Comune","#f-note":"Note"}',
    "servizio-valutazioni.html": '{"#f-tipo":"Tipo","#f-comune":"Comune","#f-note":"Note"}',
    "servizio-locazioni.html": '{"#f-comune":"Comune","#f-note":"Note"}',
    "servizio-gestione.html": '{"#f-comune":"Comune","#f-note":"Note"}',
    "servizio-preliminari.html": '{"#f-note":"Note"}',
    "servizio-utenze.html": '{"#f-note":"Note"}',
    "servizio-virtual-tour.html": '{"#f-note":"Note"}',
    "landing-vendere-casa-padova.html": '{"#f-zona":"Zona","#f-tipo":"Tipologia","#f-note":"Note"}',
}

SENDFORM_BLOCK = re.compile(
    r"<script>\s*async function sendForm\(\).*?</script>\s*",
    re.DOTALL | re.IGNORECASE,
)

INLINE_SEND_BLOCK = re.compile(
    r"<script>\s*async function send(?:Lead|MutuoLead|ConsulenzaForm)\(.*?</script>\s*",
    re.DOTALL,
)


def slug_from_blog(path: Path) -> str:
    return path.stem  # blog-foo -> provenienza blog-foo


def ensure_lead_scripts(html: str) -> str:
    if "rig-lead-form.js" in html:
        # Rimuovi defer da config se presente nella triade lead
        html = re.sub(
            r'<script src="js/config\.js\?v=\d+" defer></script>',
            '<script src="js/config.js?v=4"></script>',
            html,
            count=1,
        )
        return html
    # Prima di nav-mobile / cookie / chatbot a fine body
    insert_before = re.search(
        r"<script src=\"js/nav-mobile\.js",
        html,
    )
    if insert_before:
        pos = insert_before.start()
        return html[:pos] + LEAD_SCRIPTS + "\n" + html[pos:]
    if "</body>" in html:
        return html.replace("</body>", LEAD_SCRIPTS + "\n</body>", 1)
    return html + "\n" + LEAD_SCRIPTS


def patch_servizio_form(html: str, filename: str) -> str:
    provenienza = filename.replace(".html", "")
    if filename.startswith("servizio-"):
        provenienza = filename.replace(".html", "")

    extra = SERVIZIO_EXTRA.get(filename, "")
    extra_attr = f' data-extra-labels=\'{extra}\'' if extra else ""

    html = SENDFORM_BLOCK.sub("", html)

    # onclick sendForm -> type submit
    html = re.sub(
        r'<button class="fsub" onclick="sendForm\(\)">',
        '<button class="fsub" type="submit">',
        html,
    )
    html = re.sub(
        r'<button class="fsub fc-submit" onclick="sendForm\(\)">',
        '<button class="fsub fc-submit" type="submit">',
        html,
    )

    if "data-rig-lead-form" not in html:
        html = re.sub(
            r"<form([^>]*?)onsubmit=\"return false;\" novalidate>",
            lambda m: f'<form{m.group(1)}data-rig-lead-form data-provenienza="{provenienza}"{extra_attr} novalidate>',
            html,
            count=1,
        )

    if "rig-lead-success" not in html:
        success = (
            '<div class="rig-lead-success">'
            "<h3>Messaggio inviato!</h3>"
            "<p>Grazie. Ti ricontattiamo entro pochi minuti durante gli orari di apertura.</p>"
            "</div>\n      "
        )
        html = html.replace("</form>", success + "</form>", 1)

    return ensure_lead_scripts(html)


def patch_blog(path: Path, html: str) -> str:
    if "data-rig-lead-form" in html:
        return ensure_lead_scripts(html)

    slug = slug_from_blog(path)
    block = BLOG_FORM_TEMPLATE.format(provenienza=slug)

    if BLOG_LEAD_CSS not in html:
        html = html.replace("</head>", f"  {BLOG_LEAD_CSS}\n</head>", 1)

    if "</main>" in html:
        html = html.replace("</main>", block + "\n</main>", 1)
    else:
        html = html.replace("<footer>", block + "\n<footer>", 1)

    return ensure_lead_scripts(html)


def fix_script_order_landing(html: str) -> str:
    """Inserisce supabase+config senza defer subito prima degli handler sendLead/sendMutuo."""
    if re.search(r"async function send(?:Lead|MutuoLead|ConsulenzaForm|inviaEmailGate)", html):
        if "rig-lead-form.js" not in html.split("async function send")[0][-800:]:
            html = re.sub(
                r"(<script>\s*async function send(?:Lead|MutuoLead|ConsulenzaForm|inviaEmailGate))",
                LEAD_SCRIPTS + "\n<script>\nasync function send",
                html,
                count=1,
            )
        html = re.sub(
            r'<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2" defer></script>\s*'
            r'<script src="js/config\.js\?v=\d+" defer></script>',
            "",
            html,
        )
        html = html.replace("config.js?v=3", "config.js?v=4")
    return html


def patch_index(html: str) -> str:
    if "data-rig-lead-form" not in html:
        html = html.replace(
            '<form id="contattoForm" onsubmit="inviaContatto(event)">',
            '<form id="contattoForm" data-rig-lead-form data-provenienza="homepage" '
            'data-fields=\'{"nome":["#cf-nome","#cf-cognome"],"tel":"#cf-tel","email":"#cf-email","msg":"#cf-msg","gdpr":"#cf-gdpr"}\' novalidate>',
            1,
        )
        gdpr = (
            '<label class="fc-privacy" style="display:flex;align-items:flex-start;gap:.5rem;margin:.5rem 0">'
            '<input type="checkbox" id="cf-gdpr" required style="margin-top:.2rem">'
            '<span>Acconsento al trattamento dei dati (GDPR). Vedi <a href="privacy">Privacy Policy</a>.</span></label>'
        )
        html = html.replace(
            '<div class="fc-privacy">Inviando il modulo',
            gdpr + '\n        <div class="fc-privacy">Inviando il modulo',
            1,
        )
        ok = """<div class="rig-lead-success" id="cf-ok" style="display:none;margin-top:1rem;padding:1rem;background:#e8f5e9;border-radius:8px;text-align:center;color:#1b5e20">
          <h3 style="font-size:1.1rem;margin-bottom:.3rem">Messaggio inviato!</h3>
          <p style="font-size:.85rem">Grazie. Ti ricontattiamo presto.</p>
        </div>"""
        html = html.replace('<div id="cf-ok"></div>', ok, 1)

    # Supabase sync prima di homepage
    if "supabase-js@2" not in html.split("homepage.js")[0]:
        html = html.replace(
            '<script src="js/config.js?v=3" defer></script>',
            LEAD_SCRIPTS + "\n",
            1,
        )
    return html


def patch_immobile_send(html: str) -> str:
    old = """  try {
    await fetch(SUPABASE_URL + '/functions/v1/send-email', {
      method: 'POST',
      headers: {'Content-Type':'application/json','Authorization':'Bearer '+SUPABASE_KEY},
      body: JSON.stringify({
        action: 'send_test',
        to_email: 'info@righettoimmobiliare.it',
        sender_email: 'info@righettoimmobiliare.it',
        sender_name: 'Righetto Immobiliare',
        subject: 'Richiesta immobile: ' + (immobile?.titolo || immobile?.codice || 'N/D') + ' — ' + nome,
        html_body: '<b>Nome:</b> ' + nome + '<br><b>Telefono:</b> ' + tel + '<br><b>Immobile:</b> ' + (immobile?.titolo||'-') + ' (' + (immobile?.codice||'-') + ')' + (msg ? '<br><b>Messaggio:</b> ' + msg : '')
      })
    });
  } catch(e) {}"""
    new = """  try {
    if (typeof SERVIZI_CONFIG !== 'undefined') {
      await SERVIZI_CONFIG.sendNotifica({
        subject: 'Nuovo contatto dal sito: ' + nome,
        html_body: '<b>Nome:</b> ' + nome + '<br><b>Telefono:</b> ' + tel +
          '<br><b>Immobile:</b> ' + (immobile?.titolo||'-') + ' (' + (immobile?.codice||'-') + ')' +
          (msg ? '<br><b>Messaggio:</b> ' + msg : '') + '<br><b>Pagina:</b> immobile',
      });
    }
  } catch(e) {}"""
    if old in html:
        html = html.replace(old, new)
    if "provenienza: 'form'" in html:
        html = html.replace("provenienza: 'form'", "provenienza: 'form-immobile'")
    return html


def process_file(path: Path, dry_run: bool) -> str | None:
    name = path.name
    if name == "admin.html":
        return None
    html = path.read_text(encoding="utf-8", errors="replace")
    orig = html

    if name.startswith("servizio-") or name == "landing-vendere-casa-padova.html":
        html = patch_servizio_form(html, name)
    elif name.startswith("blog-") and name != "blog-articolo.html":
        html = patch_blog(path, html)
    elif name.startswith("landing-") or name == "vendere-casa-padova-errori.html":
        html = fix_script_order_landing(html)
        if "send-email" in html and "config.js" in html:
            html = ensure_lead_scripts(html)
    elif name == "index.html":
        html = patch_index(html)
    elif name == "immobile.html":
        html = patch_immobile_send(html)
    elif name == "contatti.html":
        html = ensure_lead_scripts(html)
    elif name == "landing-consulenza-immobiliare-gratuita.html":
        html = ensure_lead_scripts(html.replace("config.js?v=3", "config.js?v=4"))

    if html == orig:
        return None
    if not dry_run:
        path.write_text(html, encoding="utf-8", newline="\n")
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    changed = []
    for path in sorted(ROOT.glob("*.html")):
        r = process_file(path, args.dry_run)
        if r:
            changed.append(r)

    print(f"{'[DRY] ' if args.dry_run else ''}Aggiornati {len(changed)} file:")
    for c in changed:
        print(f"  - {c}")


if __name__ == "__main__":
    main()
