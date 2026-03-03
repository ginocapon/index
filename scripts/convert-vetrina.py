#!/usr/bin/env python3
"""
Converti foto vetrina in WebP ottimizzato con correzione colore.
Riduce i toni rossi, rende i colori piu' morbidi e naturali, aumenta la nitidezza.

USO:
  python3 scripts/convert-vetrina.py foto-originale.jpg

Output: img/blog/ufficio-righetto-immobiliare.webp
        img/blog/ufficio-righetto-immobiliare.jpg (backup ottimizzato)
"""

import sys
import os
from PIL import Image, ImageEnhance, ImageFilter

def process_image(input_path):
    """Processa l'immagine della vetrina con correzioni colore e nitidezza."""

    img = Image.open(input_path).convert('RGB')

    # 1. Riduci toni rossi: separa i canali e attenua il rosso
    r, g, b = img.split()
    # Riduce il canale rosso del 8% e aumenta leggermente il blu per toni piu' freddi/naturali
    r = r.point(lambda x: int(x * 0.92))
    b = b.point(lambda x: min(255, int(x * 1.04)))
    img = Image.merge('RGB', (r, g, b))

    # 2. Colori piu' morbidi: riduci leggermente la saturazione
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.85)  # 85% saturazione = piu' morbido

    # 3. Luce naturale: aumenta leggermente la luminosita'
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.06)  # +6% luminosita'

    # 4. Nitidezza: applica sharpening
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.4)  # +40% nitidezza

    # 5. Contrasto leggero per definizione
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)  # +5% contrasto

    # Percorso output
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    blog_dir = os.path.join(base_dir, 'img', 'blog')
    os.makedirs(blog_dir, exist_ok=True)

    # Ridimensiona per web (max 1200px larghezza, mantieni proporzioni)
    max_width = 1200
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    # Salva WebP (qualita' alta, ottimizzato per web)
    webp_path = os.path.join(blog_dir, 'ufficio-righetto-immobiliare.webp')
    img.save(webp_path, 'WEBP', quality=82, method=6)

    # Salva anche JPG di backup
    jpg_path = os.path.join(blog_dir, 'ufficio-righetto-immobiliare.jpg')
    img.save(jpg_path, 'JPEG', quality=85, optimize=True)

    # Dimensioni file
    webp_size = os.path.getsize(webp_path) / 1024
    jpg_size = os.path.getsize(jpg_path) / 1024

    print(f'Immagine processata con successo!')
    print(f'  Dimensioni: {img.width}x{img.height}px')
    print(f'  WebP: {webp_path} ({webp_size:.0f} KB)')
    print(f'  JPG:  {jpg_path} ({jpg_size:.0f} KB)')
    print(f'  Risparmio WebP vs JPG: {((jpg_size-webp_size)/jpg_size*100):.0f}%')
    print(f'\nCorrezioni applicate:')
    print(f'  - Canale rosso ridotto del 8%')
    print(f'  - Canale blu aumentato del 4%')
    print(f'  - Saturazione al 85% (colori piu morbidi)')
    print(f'  - Luminosita +6% (luce naturale)')
    print(f'  - Nitidezza +40%')
    print(f'  - Contrasto +5%')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python3 scripts/convert-vetrina.py <foto-originale.jpg>')
        print('La foto verra salvata in img/blog/ufficio-righetto-immobiliare.webp')
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f'Errore: file non trovato: {input_path}')
        sys.exit(1)

    process_image(input_path)
