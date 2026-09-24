#!/usr/bin/env python3
"""Génère index.html, contact.vcf et qr.png à partir de CONFIG.

Changer de nom = modifier CONFIG["name"] (et éventuellement "domain"/"email"),
puis relancer :  python3 build.py
"""
import pathlib, html

CONFIG = {
    "name": "Hailp",                       # ← le nom de la boîte, en 1 ligne
    "tagline": "Conseil et agents IA sur-mesure",
    "url": "https://hailp.tech",
    "qr_url": "https://alexwattel1.github.io",  # QR volontairement sur l’URL neutre : redirige vers hailp.tech, survit à un changement de domaine
    "person": "Alexandre Wattel",
    "role": "Fondateur · Conseil et agents IA",
    "phone": "+33 6 58 43 88 24",
    "phone_raw": "+33658438824",
    "email": "alexandre.wattel1@gmail.com",  # → alexandre@<domaine> une fois la redirection OVH active
    "linkedin": "https://www.linkedin.com/in/alexandre-wattel-652303a8/",
    "city": "Lyon",
    "aimpct": "https://ai-mpct.com",
    "calendly": "https://calendly.com/alexandre-wattel1/30min",
}

ROOT = pathlib.Path(__file__).parent


def vcard(c):
    first, last = c["person"].split(" ", 1)
    return "\r\n".join([
        "BEGIN:VCARD", "VERSION:3.0",
        f"N:{last};{first};;;", f"FN:{c['person']}",
        f"ORG:{c['name']}", f"TITLE:{c['role'].replace('·', '-')}",
        f"TEL;TYPE=CELL:{c['phone_raw']}", f"EMAIL;TYPE=WORK:{c['email']}",
        f"URL:{c['url']}", f"X-SOCIALPROFILE;TYPE=linkedin:{c['linkedin']}",
        f"ADR;TYPE=WORK:;;;{c['city']};;;France",
        f"NOTE:{c['tagline']}. Rencontré via le QR code.",
        "END:VCARD", "",
    ])


def page(c):
    e = {k: html.escape(v) for k, v in c.items()}
    return (ROOT / "template.html").read_text(encoding="utf-8").format(**e)


def qr(c):
    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=2)
    q.add_data(c["qr_url"])
    q.make(fit=True)
    q.make_image(fill_color="#0B1B24", back_color="white").save(ROOT / "qr.png")


if __name__ == "__main__":
    (ROOT / "index.html").write_text(page(CONFIG), encoding="utf-8")
    (ROOT / "contact.vcf").write_text(vcard(CONFIG), encoding="utf-8")
    qr(CONFIG)
    print("OK →", CONFIG["name"], "|", CONFIG["url"])
