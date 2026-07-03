#!/usr/bin/env python3
"""Inietta JSON-LD RealEstateAgent su blog che ne sono privi."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AGENT_BLOCK = """
  <!-- JSON-LD RealEstateAgent -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "RealEstateAgent",
    "name": "Gruppo Immobiliare Righetto di Capon Gino",
    "url": "https://righettoimmobiliare.it",
    "telephone": "+390498843484",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Via Roma n.96",
      "addressLocality": "Limena",
      "postalCode": "35010",
      "addressRegion": "PD",
      "addressCountry": "IT"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 45.476956,
      "longitude": 11.845762
    },
    "sameAs": [
      "https://www.facebook.com/righettoimmobiliare",
      "https://www.instagram.com/righettoimmobiliare",
      "https://www.linkedin.com/company/righetto-immobiliare"
    ],
    "hasMap": "https://maps.google.com/?q=45.476956,11.845762",
    "areaServed": [
      {"@type": "City", "name": "Padova"},
      {"@type": "City", "name": "Limena"},
      {"@type": "City", "name": "Vigonza"},
      {"@type": "City", "name": "Campodarsego"},
      {"@type": "City", "name": "Selvazzano Dentro"},
      {"@type": "City", "name": "Abano Terme"},
      {"@type": "City", "name": "Rubano"},
      {"@type": "City", "name": "Villafranca Padovana"}
    ],
    "foundingDate": "2000",
    "priceRange": "$$"
  }
  </script>
"""


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if '"@type": "RealEstateAgent"' in text or '"RealEstateAgent"' in text:
        return False
    marker = "  <style>"
    if marker not in text:
        marker = "</head>"
    if marker not in text:
        return False
    if AGENT_BLOCK.strip() in text:
        return False
    new_text = text.replace(marker, AGENT_BLOCK + "\n" + marker, 1)
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    n = 0
    targets = sorted(ROOT.glob("blog-*.html"))
    targets += sorted(ROOT.glob("share-immobile-*.html"))
    for extra in ("privacy.html", "privacy-policy.html", "cookie-policy.html", "visita-virtuale.html"):
        p = ROOT / extra
        if p.exists():
            targets.append(p)
    for p in targets:
        if patch(p):
            n += 1
            print("patched", p.name)
    print(f"Done: {n} blog aggiornati")


if __name__ == "__main__":
    main()
