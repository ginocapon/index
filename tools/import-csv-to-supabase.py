#!/usr/bin/env python3
"""
Importa contatti da CSV nella tabella 'clienti' di Supabase.

Uso:
  python3 tools/import-csv-to-supabase.py contatti.csv

Il CSV deve avere come prima riga l'intestazione con almeno la colonna "Email".
Le colonne riconosciute sono (case-insensitive):
  - Cognome, Nome, Ragione sociale
  - Email, Email PEC
  - Telefono, Cellulare
  - Partita IVA, Cod. Fiscale (o Codice Fiscale)
  - Stato, Provincia, Comune, Zona, Indirizzo, Civico, Cap
  - codice SDI
  - Note
  - Agente
"""

import csv
import json
import re
import sys
import time
import requests

# ── Configurazione Supabase ──────────────────────────────
SUPABASE_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc"
TABLE = "clienti"
BATCH_SIZE = 50

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal,resolution=merge-duplicates"
}


def clean_phone(val):
    """Normalizza numero di telefono: rimuove spazi e caratteri extra."""
    if not val:
        return None
    # Il CSV potrebbe avere numeri in notazione scientifica (3,49E+09)
    val = val.strip().replace('\xa0', '')
    if 'E+' in val.upper() or 'e+' in val.lower():
        try:
            num = int(float(val.replace(',', '.')))
            return str(num)
        except (ValueError, OverflowError):
            return None
    # Rimuovi tutto tranne cifre e +
    cleaned = re.sub(r'[^\d+]', '', val)
    return cleaned if len(cleaned) >= 6 else None


def clean_email(val):
    """Valida e pulisce un indirizzo email."""
    if not val:
        return None
    val = val.strip().lower().rstrip('.')
    # Correggi errori comuni
    val = val.replace('gmial.com', 'gmail.com')
    if re.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', val):
        return val
    return None


def build_address(row, col_map):
    """Compone l'indirizzo completo da indirizzo + civico + cap + comune."""
    parts = []
    for field in ['Indirizzo', 'Civico']:
        k = col_map.get(field.lower())
        if k and row.get(k, '').strip():
            parts.append(row[k].strip())
    addr = ', '.join(parts)
    cap = row.get(col_map.get('cap', ''), '').strip()
    comune = row.get(col_map.get('comune', ''), '').strip()
    provincia = row.get(col_map.get('provincia', ''), '').strip()
    if cap:
        addr += f' - {cap}'
    if comune:
        addr += f' {comune}'
    if provincia:
        addr += f' ({provincia})'
    return addr.strip(' -,') or None


def detect_delimiter(filepath):
    """Rileva automaticamente il delimitatore CSV."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        sample = f.read(4096)
    for delim in ['\t', ';', ',']:
        if delim in sample:
            count = sample.count(delim)
            if count > 5:
                return delim
    return ','


def parse_csv(filepath):
    """Legge il CSV e ritorna una lista di record pronti per Supabase."""
    delimiter = detect_delimiter(filepath)
    print(f"Delimitatore rilevato: {repr(delimiter)}")

    contacts = []
    seen_emails = set()

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f, delimiter=delimiter)

        # Mappa colonne CSV -> campi Supabase
        fieldnames = [fn.strip() for fn in (reader.fieldnames or [])]
        col_map = {}
        for fn in fieldnames:
            fl = fn.lower().strip()
            if 'cognome' in fl:
                col_map['cognome'] = fn
            elif fl == 'nome':
                col_map['nome'] = fn
            elif 'ragione' in fl:
                col_map['ragione_sociale'] = fn
            elif fl == 'email' or fl == 'e-mail':
                col_map['email'] = fn
            elif 'email pec' in fl or 'pec' in fl:
                col_map['pec'] = fn
            elif fl == 'telefono':
                col_map['telefono'] = fn
            elif fl == 'cellulare' or fl == 'cell':
                col_map['cellulare'] = fn
            elif 'partita' in fl or 'p.iva' in fl:
                col_map['partita_iva'] = fn
            elif 'fiscale' in fl:
                col_map['codice_fiscale'] = fn
            elif fl == 'stato':
                col_map['stato'] = fn
            elif fl == 'provincia':
                col_map['provincia'] = fn
            elif fl == 'comune':
                col_map['comune'] = fn
            elif fl == 'zona':
                col_map['zona'] = fn
            elif fl == 'indirizzo':
                col_map['indirizzo'] = fn
            elif fl == 'civico':
                col_map['civico'] = fn
            elif fl == 'cap':
                col_map['cap'] = fn
            elif 'sdi' in fl:
                col_map['sdi'] = fn
            elif fl == 'note':
                col_map['note'] = fn
            elif fl == 'agente':
                col_map['agente'] = fn

        print(f"Colonne mappate: {list(col_map.keys())}")

        for row in reader:
            # Salta righe header duplicate
            email_col = col_map.get('email')
            if not email_col:
                continue
            raw_email = row.get(email_col, '').strip()
            if not raw_email or raw_email.lower() in ('email', 'e-mail'):
                continue

            email = clean_email(raw_email)
            if not email:
                continue

            # Skip duplicati
            if email in seen_emails:
                continue
            seen_emails.add(email)

            # Skip email di sistema/PEC-only
            skip_patterns = ['@pec.', '@legalmail.', '@arubapec.', '@comune.', 'disdette@']
            if any(p in email for p in skip_patterns):
                continue

            # Componi nome
            cognome = row.get(col_map.get('cognome', ''), '').strip()
            nome = row.get(col_map.get('nome', ''), '').strip()
            full_name = f"{cognome} {nome}".strip()
            if not full_name or full_name.lower() in ('cognome nome', 'cognome', 'nome'):
                full_name = email.split('@')[0].replace('.', ' ').replace('_', ' ').title()

            # Telefono: preferisci cellulare
            telefono = clean_phone(row.get(col_map.get('cellulare', ''), ''))
            if not telefono:
                telefono = clean_phone(row.get(col_map.get('telefono', ''), ''))

            # PEC
            pec_col = col_map.get('pec')
            pec = clean_email(row.get(pec_col, '')) if pec_col else None

            # Note
            note_col = col_map.get('note')
            note = row.get(note_col, '').strip()[:1000] if note_col else None

            # Indirizzo
            indirizzo = build_address(row, col_map)

            # Codice fiscale
            cf_col = col_map.get('codice_fiscale')
            cf = row.get(cf_col, '').strip() if cf_col else None
            if cf and len(cf) != 16:
                cf = None

            # Partita IVA
            piva_col = col_map.get('partita_iva')
            piva = row.get(piva_col, '').strip() if piva_col else None

            # Ragione sociale
            rs_col = col_map.get('ragione_sociale')
            rs = row.get(rs_col, '').strip() if rs_col else None

            # SDI
            sdi_col = col_map.get('sdi')
            sdi = row.get(sdi_col, '').strip() if sdi_col else None

            # Tipo cliente
            tipo = 'azienda' if rs or piva else 'privato'

            record = {
                'nome': full_name,
                'email': email,
                'telefono': telefono,
                'note': note or None,
                'codice_fiscale': cf,
                'indirizzo_cliente': indirizzo,
                'ragione_sociale': rs or None,
                'partita_iva': piva or None,
                'pec': pec,
                'sdi': sdi or None,
                'tipo_cliente': tipo,
                'fonte': 'import_csv'
            }

            # Rimuovi campi None
            record = {k: v for k, v in record.items() if v is not None}
            contacts.append(record)

    return contacts


def upload_batch(records, batch_num, total_batches):
    """Carica un batch di record su Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/{TABLE}"
    r = requests.post(url, headers=HEADERS, json=records)
    if r.status_code in (200, 201):
        print(f"  Batch {batch_num}/{total_batches}: {len(records)} record caricati OK")
        return len(records)
    else:
        print(f"  Batch {batch_num}/{total_batches}: ERRORE {r.status_code} - {r.text[:200]}")
        # Prova uno a uno
        ok = 0
        for rec in records:
            r2 = requests.post(url, headers=HEADERS, json=rec)
            if r2.status_code in (200, 201):
                ok += 1
            else:
                print(f"    SKIP {rec.get('email')}: {r2.text[:100]}")
        print(f"    Recuperati {ok}/{len(records)} record singolarmente")
        return ok


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 tools/import-csv-to-supabase.py <file.csv>")
        print("")
        print("Il CSV deve avere intestazione con almeno 'Email' come colonna.")
        print("Colonne opzionali: Cognome, Nome, Cellulare, Telefono, Note, ecc.")
        sys.exit(1)

    filepath = sys.argv[1]
    print(f"\n{'='*60}")
    print(f"  IMPORT CSV -> SUPABASE (tabella: {TABLE})")
    print(f"{'='*60}")
    print(f"File: {filepath}\n")

    contacts = parse_csv(filepath)
    print(f"\nContatti validi trovati: {len(contacts)}")

    if not contacts:
        print("Nessun contatto valido trovato nel CSV.")
        sys.exit(0)

    # Mostra anteprima
    print(f"\nAnteprima primi 3 contatti:")
    for c in contacts[:3]:
        print(f"  {c.get('nome', '?')} <{c.get('email', '?')}> tel:{c.get('telefono', '-')}")

    # Conferma
    resp = input(f"\nCaricare {len(contacts)} contatti su Supabase? (s/n): ").strip().lower()
    if resp not in ('s', 'si', 'y', 'yes'):
        print("Annullato.")
        sys.exit(0)

    # Upload in batch
    total_uploaded = 0
    batches = [contacts[i:i+BATCH_SIZE] for i in range(0, len(contacts), BATCH_SIZE)]
    total_batches = len(batches)

    print(f"\nInvio {total_batches} batch da max {BATCH_SIZE} record...\n")

    for i, batch in enumerate(batches, 1):
        uploaded = upload_batch(batch, i, total_batches)
        total_uploaded += uploaded
        if i < total_batches:
            time.sleep(0.3)

    print(f"\n{'='*60}")
    print(f"  COMPLETATO: {total_uploaded}/{len(contacts)} contatti caricati")
    print(f"{'='*60}")
    print(f"\nOra puoi andare nell'admin -> Email Marketing -> 'Carica da Clienti'")


if __name__ == '__main__':
    main()
