#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Promemoria email ogni ~15 giorni — Guardian + LINDA Learning Bridge.
Usa lo stesso relay del venerdì (send-mail.php + EMAIL_RELAY_KEY) — zero API a pagamento.

Output: guardian-biweekly-email.html, guardian-biweekly-subject.txt
Cron: .github/workflows/guardian-learning-bridge-biweekly.yml
"""
from __future__ import annotations

import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LB_DIR = ROOT / "data" / "learning-bridge"
OUT_HTML = ROOT / "guardian-biweekly-email.html"
OUT_SUBJECT = ROOT / "guardian-biweekly-subject.txt"


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def metrics_block() -> str:
    report = load_json(LB_DIR / "learning-report.json", {})
    insights = load_json(LB_DIR / "ranking-insights.json", {})
    evaluation = load_json(LB_DIR / "evaluation-latest.json", {})

    lines = ["<h3 style='color:#2c4a6e;margin-top:1.2em'>Dati dall'ultima analisi in repo</h3>"]
    if not report and not insights and not evaluation:
        lines.append(
            "<p><em>Nessun report locale ancora — normale se non hai lanciato "
            "<code>learning biweekly</code> sul PC. Linda raccoglie eventi sul sito in automatico.</em></p>"
        )
        return "\n".join(lines)

    if report:
        lines.append(
            f"<p><strong>Eventi analizzati:</strong> {escape(str(report.get('total_events', '—')))} · "
            f"<strong>Bucket sufficienti:</strong> {escape(str(report.get('sufficient_buckets', '—')))}</p>"
        )
    if insights:
        n = len(insights.get("ranking_insights") or [])
        lines.append(f"<p><strong>Insight ranking:</strong> {n}</p>")
    if evaluation:
        lines.append(
            f"<p><strong>Raccomandazione evaluation:</strong> "
            f"{escape(str(evaluation.get('recommendation', '—')))} · "
            f"<strong>Ranking attivo:</strong> {escape(str(evaluation.get('active_ranking', 'baseline_v1')))}</p>"
        )
    return "\n".join(lines)


def build_html(today: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="it">
<head><meta charset="utf-8"><title>Promemoria Guardian</title></head>
<body style="font-family:Montserrat,Arial,sans-serif;font-size:15px;line-height:1.55;color:#152435;max-width:640px;margin:0 auto;padding:20px">
  <p style="font-size:12px;color:#6b7a8d">Righetto Immobiliare · Premortem Guardian + LINDA Learning Bridge</p>
  <h1 style="font-size:1.35rem;color:#2c4a6e">Promemoria ogni 15 giorni — Guardian &amp; Learning</h1>
  <p><strong>Data:</strong> {escape(today)}</p>

  <h2 style="font-size:1.1rem;color:#2c4a6e">Cosa fa il sistema (in automatico sul sito)</h2>
  <ul>
    <li><strong>Linda</strong> raccoglie eventi anonimi: ricerche, click annunci, lead, domande senza risposta, abbandoni.</li>
    <li><strong>Non modifica</strong> prezzi, annunci o ranking live (<code>apply_ranking_changes: false</code>).</li>
    <li>Il database immobili resta l'unica fonte di verità.</li>
  </ul>

  <h2 style="font-size:1.1rem;color:#2c4a6e">Cosa fare tu ora (sul PC, ~5 minuti)</h2>
  <ol>
    <li>Apri PowerShell nella cartella del progetto:<br>
      <code style="background:#f4f1ec;padding:4px 8px;border-radius:4px">cd C:\\Users\\Utente\\GitHub\\index</code></li>
    <li>Aggiorna il codice: <code>git pull</code></li>
    <li>Lancia l'analisi:<br>
      <code style="background:#f4f1ec;padding:4px 8px;border-radius:4px">node .\\righetto-premortem-guardian\\scripts\\guardian.mjs learning biweekly</code></li>
    <li>Leggi i report in <code>data\\learning-bridge\\</code> (JSON).</li>
    <li>In chat Cursor scrivi: <strong>GUARDIAN</strong> o <strong>LEARNING BRIDGE</strong> — l'agente legge i report e ti propone azioni (FAQ, blog, SEO).</li>
  </ol>

  {metrics_block()}

  <h2 style="font-size:1.1rem;color:#2c4a6e">Ciclo controllato (ricorda)</h2>
  <p style="background:#f7f5f1;padding:12px;border-left:4px solid #2c4a6e">
    OSSERVA → ANALISI → INSIGHT → PROPOSTA → TEST → MISURA → (solo se OK) APPLICA → ROLLBACK se peggiora
  </p>

  <h2 style="font-size:1.1rem;color:#2c4a6e">Comandi utili</h2>
  <ul>
    <li><code>guardian.mjs doctor</code> — controllo installazione</li>
    <li><code>guardian.mjs learning full</code> — report completo (mensile)</li>
    <li><code>guardian.mjs run</code> — premortem Guardian</li>
  </ul>

  <p style="font-size:13px;color:#6b7a8d;margin-top:2em">
    Informativa: <a href="https://righettoimmobiliare.it/privacy#trasparenza-digitale">privacy#trasparenza-digitale</a> ·
    Skill: <code>righetto-premortem-guardian/skill/SKILL.md</code>
  </p>
</body>
</html>"""


def main() -> None:
    today = date.today().strftime("%d/%m/%Y")
    subject = f"Promemoria Guardian + Learning Bridge — {today} (ogni 15 giorni)"
    OUT_HTML.write_text(build_html(today), encoding="utf-8")
    OUT_SUBJECT.write_text(subject, encoding="utf-8")
    print(f"OK: {OUT_HTML.name}, {OUT_SUBJECT.name}")


if __name__ == "__main__":
    main()
