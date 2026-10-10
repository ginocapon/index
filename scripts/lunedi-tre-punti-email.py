#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email richiamo «3 task» per Gino (stile report test / venerdì).
Output: lunedi-email-report.html, lunedi-email-subject.txt
Cron: .github/workflows/martedi-tre-punti-agente.yml (martedì 07:00 CEST)
"""
from __future__ import annotations

import json
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "lunedi-tre-punti-reminder.json"
OUT_HTML = ROOT / "lunedi-email-report.html"
OUT_SUBJECT = ROOT / "lunedi-email-subject.txt"


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    today = date.today().strftime("%d/%m/%Y")
    scheduled = payload.get("scheduled_for", "—")
    weekday = payload.get("scheduled_weekday", "martedì")
    prefix = payload.get("email_subject_prefix", "[TEST] Piano agente")

    tasks_html = []
    for t in payload.get("tasks", []):
        tasks_html.append(
            f"<li><strong>{escape(t['title'])}</strong><br>{escape(t['body'])}</li>"
        )
    parallel = payload.get("parallel_non_blocking", [])
    par_html = "".join(f"<li>{escape(x)}</li>" for x in parallel)

    html = f"""<!DOCTYPE html>
<html lang="it">
<head><meta charset="utf-8"><title>Piano lunedì — 3 task</title></head>
<body style="font-family:Montserrat,Arial,sans-serif;font-size:15px;line-height:1.55;color:#152435;max-width:640px;margin:0 auto;padding:20px">
  <p style="font-size:12px;color:#6b7a8d">Righetto Immobiliare · Richiamo agente Cloud · <strong>TEST</strong> (come report venerdì)</p>
  <h1 style="font-size:1.35rem;color:#2c4a6e">{escape(weekday.capitalize())} — i 3 task da gestire</h1>
  <p><strong>Oggi:</strong> {escape(today)} · <strong>Piano per:</strong> {escape(scheduled)} ({escape(weekday)})</p>
  <p>Quando chiedi in chat «cosa dobbiamo fare» o «i tre punti», l'agente usa la stessa lista.</p>

  <h2 style="font-size:1.1rem;color:#2c4a6e">Priorità (ordine consigliato)</h2>
  <ol style="padding-left:1.2em">
    {''.join(tasks_html)}
  </ol>

  <h2 style="font-size:1.1rem;color:#2c4a6e">In parallelo (non blocca SEO)</h2>
  <ul>{par_html}</ul>

  <p style="font-size:13px;color:#6b7a8d;margin-top:2em">
    Fonte repo: <code>data/lunedi-tre-punti-reminder.json</code> ·
    Workflow: <code>martedi-tre-punti-agente.yml</code>
  </p>
</body>
</html>"""

    subject = f"{prefix} — {today}"
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_SUBJECT.write_text(subject, encoding="utf-8")
    print(f"OK: {OUT_HTML.name}, {OUT_SUBJECT.name}")
    print(f"Subject: {subject}")


if __name__ == "__main__":
    main()
