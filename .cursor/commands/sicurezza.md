# Revisione sicurezza

Leggi e applica `.cursor/skills/righetto-security/SKILL.md`.

Esegui: `bash scripts/security-check.sh` e `python tools/check_rls_exposure.py` (se `.env` disponibile).

Output: checklist §3 con stato ✅/❌ e azioni prioritarie. Fix solo su issue confermati.

Mai committare segreti.
