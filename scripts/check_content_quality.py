#!/usr/bin/env python3
"""Controllo offline di completezza. Non pubblica, non apre connessioni."""
import json,sys
from pathlib import Path
REQUIRED=('id','canale','persona','problema','apertura','corpo','cta','destinazione','fonti','stato','metrica')
def check(item):
 errors=[]
 for key in REQUIRED:
  if not item.get(key): errors.append('manca '+key)
 if item.get('pubblicazione_abilitata') is not False: errors.append('abilitazione uscita non consentita nelle bozze')
 if item.get('canale') in ('instagram','facebook'):
  caption=item.get('apertura','')+' '+item.get('corpo','')+' '+item.get('cta','')
  if 'http' in caption or 'www.' in caption: errors.append('link nella caption Meta')
  if '{' in caption or '}' in caption: errors.append('spintax non risolto')
 if not item.get('fonti'): errors.append('fonti non documentate')
 return errors
if __name__=='__main__':
 data=json.loads(Path(sys.argv[1]).read_text()); bad=0
 for item in data['items']:
  errors=check(item);bad+=bool(errors)
  print(item.get('id','senza_id')+': '+('; '.join(errors) if errors else 'scheda completa, resta BOZZA'))
 print('Validazione strutturale soltanto: non prova verità dei dati, diritti dei media, approvazione o pubblicazione.')
 raise SystemExit(bool(bad))
