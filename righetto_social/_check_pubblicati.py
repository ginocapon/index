#!/usr/bin/env python3
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
import os
from supabase import create_client

tz = ZoneInfo("Europe/Rome")
now = datetime.now(tz)
today = now.date().isoformat()
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

print("ORA:", now.strftime("%Y-%m-%d %H:%M"), "\n")

for day in [today, (now.date() - timedelta(days=1)).isoformat()]:
    r = (
        sb.table("pianificazioni")
        .select("ora,tipo,contenuto,titolo,note")
        .eq("data_inizio", day)
        .order("ora")
        .execute()
    )
    rows = r.data or []
    pub = [x for x in rows if "PUB_OK" in str(x.get("note") or "")]
    err = [x for x in rows if "PUB_ERR" in str(x.get("note") or "")]
    pend = [x for x in rows if "PUB_OK" not in str(x.get("note") or "") and "PUB_ERR" not in str(x.get("note") or "")]
    print(f"=== {day} ===")
    print(f"Totale {len(rows)} | OK {len(pub)} | ERR {len(err)} | In attesa {len(pend)}")
    for x in sorted(pub, key=lambda z: z["ora"]):
        n = str(x.get("note") or "")
        stamp = n.split("PUB_OK")[-1][:40] if "PUB_OK" in n else ""
        print(f"  OK  {x['ora'][:5]} {x['tipo'][:14]:14} {(x.get('titolo') or '')[:42]}")
    for x in sorted(err, key=lambda z: z["ora"]):
        print(f"  ERR {x['ora'][:5]} {x['tipo'][:14]:14} {(x.get('titolo') or '')[:35]}")
        print(f"       {str(x.get('note') or '')[-120:]}")
    for x in sorted(pend, key=lambda z: z["ora"]):
        if x["ora"][:5] <= now.strftime("%H:%M")[:5]:
            print(f"  MANCA {x['ora'][:5]} {x['tipo'][:14]:14} {(x.get('titolo') or '')[:42]}")
    print()
