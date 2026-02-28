#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║  GENERA VOCE SARA — Righetto Immobiliare                ║
║  Usa Microsoft Neural TTS (gratuito, ultra-realistico)  ║
╚══════════════════════════════════════════════════════════╝

Requisiti:
  pip install edge-tts

Uso:
  python3 scripts/generate-voice.py

Genera: audio/welcome-sara.mp3

Voci disponibili (italiane femminili neurali):
  - it-IT-ElsaNeural     → professionale, chiara
  - it-IT-IsabellaNeural → calda, naturale (DEFAULT)
"""

import asyncio
import sys
import os

try:
    import edge_tts
except ImportError:
    print("❌ Installa edge-tts: pip install edge-tts")
    sys.exit(1)

# ── Configurazione ──
VOICE = "it-IT-IsabellaNeural"   # Voce calda e naturale
RATE = "-5%"                      # Leggermente più lenta (più naturale)
PITCH = "+2Hz"                    # Tono leggermente più alto (femminile)
VOLUME = "+0%"

# ── Testo con SSML per pause naturali ──
TEXT = """Ciao! Sono Sara, la tua assistente virtuale di Righetto Immobiliare.

Dal 2000 aiutiamo chi cerca, vende o affitta casa a Padova e in tutta la provincia.

Qui trovi valutazioni gratuite, consulenza su vendita e locazione, gestione completa del tuo immobile e molto altro.

Se hai domande, la nostra chatbot è pronta a risponderti subito! E per tutto il resto, i nostri consulenti sono sempre a disposizione.

Scegli come vuoi continuare!"""

OUTPUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio", "welcome-sara.mp3")


async def main():
    print(f"🎙️  Voce: {VOICE}")
    print(f"📝  Testo: {len(TEXT)} caratteri")
    print(f"📁  Output: {OUTPUT}")
    print()

    # Assicura che la directory esista
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    communicate = edge_tts.Communicate(
        TEXT,
        VOICE,
        rate=RATE,
        pitch=PITCH,
        volume=VOLUME
    )

    print("⏳  Generazione in corso...")
    await communicate.save(OUTPUT)

    size = os.path.getsize(OUTPUT)
    print(f"✅  Fatto! {OUTPUT} ({size / 1024:.0f} KB)")
    print()
    print("🔊  Testa con: open audio/welcome-sara.mp3  (macOS)")
    print("              xdg-open audio/welcome-sara.mp3  (Linux)")


if __name__ == "__main__":
    # Opzione: scegli voce da linea di comando
    if len(sys.argv) > 1 and sys.argv[1] == "--elsa":
        VOICE = "it-IT-ElsaNeural"
        print("🎭  Usando voce ElsaNeural (più formale)")
    elif len(sys.argv) > 1 and sys.argv[1] == "--list":
        async def list_voices():
            voices = await edge_tts.list_voices()
            print("🇮🇹  Voci italiane disponibili:")
            for v in voices:
                if "it-IT" in v.get("Locale", ""):
                    print(f"   {v['ShortName']:30s} {v['Gender']:10s}")
        asyncio.run(list_voices())
        sys.exit(0)

    asyncio.run(main())
