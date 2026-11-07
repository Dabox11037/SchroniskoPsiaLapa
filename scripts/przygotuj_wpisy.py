# -*- coding: utf-8 -*-
"""
Przygotowanie nowych artykułów bloga.

Wrzuć artykuł (samą treść HTML, bez nagłówka) do folderu blog/wpisy/
pod dowolną nazwą, a potem uruchom:

    python scripts/przygotuj_wpisy.py

Dla każdego pliku bez nagłówka skrypt zapyta o:
  tytuł, opis, datę, autora, obrazek okładki i teksty alt zdjęć.
W wpisach już przygotowanych uzupełnia brakujące teksty alt.
W nawiasach [ ] pokazuje podpowiedź – Enter ją akceptuje.
Potem dopisuje nagłówek, zmienia nazwę pliku na adres z tytułu
(np. jak-wybrac-psa-ai.html) i generuje blog (generuj_bloga.py).
"""
import html
import os
import re
import sys
import unicodedata
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generuj_produkty import ROOT, SITE  # noqa: E402

SRC_DIR = os.path.join(ROOT, "blog", "wpisy")
PL = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")

# Windows: polskie znaki w terminalu
for stream in (sys.stdin, sys.stdout):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass


def slugify(text):
    text = unicodedata.normalize("NFKD", text.translate(PL)).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(text) > 60:
        cut = text[:61]
        text = cut[: cut.rfind("-")] if "-" in cut else text[:60]
    return text.strip("-") or "wpis"


def plain(fragment):
    text = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def has_header(raw):
    return bool(re.match(r"\s*<!--.*?tytul\s*:", raw.lstrip("﻿"), re.S))


def suggest_title(filename):
    name = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").strip()
    return name[:1].upper() + name[1:]


def suggest_desc(body):
    m = re.search(r"<p[^>]*>(.*?)</p>", body, re.S)
    text = plain(m.group(1)) if m else plain(body)
    if len(text) <= 155:
        return text
    cut = text[:155]
    cut = cut[: cut.rfind(" ")] if " " in cut else cut
    return cut.rstrip(",;:–- ") + "…"


def suggest_image(body):
    m = re.search(r'<img[^>]+src="([^"]+)"', body)
    if not m:
        return ""
    src = m.group(1)
    return src[len(SITE):] if src.startswith(SITE) else src


def ask(label, default="", required=True, check=None):
    while True:
        hint = f" [{default}]" if default else ""
        value = input(f"  {label}{hint}: ").strip() or default
        if not value and required:
            print("    ✗ To pole jest wymagane.")
            continue
        if value and check:
            err = check(value)
            if err:
                print(f"    ✗ {err}")
                continue
        return value


def check_date(v):
    try:
        date.fromisoformat(v)
    except ValueError:
        return "Podaj datę w formacie RRRR-MM-DD, np. 2026-11-07."


def check_image(v):
    if v.startswith("http"):
        return None
    if not os.path.exists(os.path.join(ROOT, v)):
        return f"Nie ma pliku {v} (ścieżka od katalogu głównego strony, np. assets/blog/okladka.jpg)."


IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
ALT_RE = re.compile(r'\salt\s*=\s*("([^"]*)"|\'([^\']*)\')', re.I)


def product_names():
    try:
        from generuj_produkty import PRODUCTS
        return {p["slug"]: p["name"] for p in PRODUCTS}
    except Exception:
        return {}


def suggest_alt(src, names):
    base = os.path.splitext(os.path.basename(src.split("?")[0]))[0]
    if base in names:
        return names[base]
    text = re.sub(r"[-_]+", " ", base).strip()
    return text[:1].upper() + text[1:]


def fix_alts(body, only_missing):
    """Pyta o tekst alt dla zdjęć. only_missing=True – tylko dla zdjęć bez alt."""
    names = product_names()
    imgs = list(IMG_RE.finditer(body))
    targets = []
    for m in imgs:
        am = ALT_RE.search(m.group(0))
        current = html.unescape(am.group(2) if am and am.group(2) is not None else (am.group(3) if am else "")) if am else ""
        if only_missing and current.strip():
            continue
        targets.append((m, am, current))
    if not targets:
        return body, 0

    print(f"\n  Teksty alt zdjęć ({len(targets)}) – opisz, co widać na zdjęciu."
          f"\n  Wpisz '-' dla zdjęcia czysto dekoracyjnego (alt pusty).")
    out, last = [], 0
    for i, (m, am, current) in enumerate(targets, 1):
        src = re.search(r'src\s*=\s*"([^"]*)"', m.group(0))
        src = src.group(1) if src else "?"
        print(f"\n  Zdjęcie {i}/{len(targets)}: {src}")
        alt = ask("Tekst alt", current.strip() or suggest_alt(src, names),
                  check=lambda v: "Usuń znak '-->'." if "-->" in v else None)
        alt = "" if alt == "-" else alt
        tag = m.group(0)
        new_attr = f' alt="{html.escape(alt, quote=True)}"'
        tag = tag[:am.start()] + new_attr + tag[am.end():] if am else re.sub(r"^<img\b", "<img" + new_attr, tag, flags=re.I)
        out.append(body[last:m.start()] + tag)
        last = m.end()
    out.append(body[last:])
    return "".join(out), len(targets)


def main():
    files = sorted(f for f in os.listdir(SRC_DIR) if f.lower().endswith(".html"))
    todo = []
    for f in files:
        path = os.path.join(SRC_DIR, f)
        raw = open(path, encoding="utf-8").read()
        if not has_header(raw):
            todo.append((f, raw.lstrip("﻿").strip()))
            continue
        # Wpisy już przygotowane: uzupełnij tylko brakujące teksty alt
        m = re.match(r"(\s*<!--.*?-->)(.*)", raw.lstrip("﻿"), re.S)
        if any(not (ALT_RE.search(t) and (ALT_RE.search(t).group(2) or ALT_RE.search(t).group(3) or "").strip())
               for t in IMG_RE.findall(m.group(2))):
            print(f"\n{f} – brakuje tekstów alt:")
            new_body, n = fix_alts(m.group(2), only_missing=True)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(m.group(1) + new_body)
            print(f"  ✓ Uzupełniono {n} tekst(ów) alt")

    if not todo:
        print("Nie ma nowych wpisów bez nagłówka.")
    for n, (f, body) in enumerate(todo, 1):
        print(f"\n[{n}/{len(todo)}] {f}")
        print(f"  Początek: {plain(body)[:120]}…\n")
        title = ask("Tytuł artykułu", suggest_title(f), check=lambda v: "Usuń znak '-->' z tytułu." if "-->" in v else None)
        desc = ask("Opis (do Google, ok. 150 znaków)", suggest_desc(body),
                   check=lambda v: "Usuń znak '-->' z opisu." if "-->" in v else None)
        when = ask("Data publikacji (RRRR-MM-DD)", date.today().isoformat(), check=check_date)
        author = ask("Autor", "Zespół Psiej Łapy")
        image = ask("Obrazek okładki (Enter = brak)", suggest_image(body), required=False, check=check_image)

        slug = ask("Adres wpisu (nazwa pliku)", slugify(title),
                   check=lambda v: None if re.fullmatch(r"[a-z0-9-]+", v) else "Tylko małe litery, cyfry i myślniki.")
        new_name = slug + ".html"
        if new_name != f and os.path.exists(os.path.join(SRC_DIR, new_name)):
            print(f"  ✗ Plik {new_name} już istnieje – pomijam ten artykuł, zmień adres i uruchom skrypt ponownie.")
            continue

        body, _ = fix_alts(body, only_missing=False)

        header = f"<!--\ntytul: {title}\nopis: {desc}\ndata: {when}\nautor: {author}\n"
        if image:
            header += f"obrazek: {image}\n"
        header += "-->\n"
        with open(os.path.join(SRC_DIR, new_name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(header + body + "\n")
        if new_name != f:
            os.remove(os.path.join(SRC_DIR, f))
        print(f"  ✓ Zapisano jako blog/wpisy/{new_name}")

    print("\nGeneruję blog…")
    import generuj_bloga
    generuj_bloga.main()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrzerwano – pliki, które nie zostały jeszcze zapisane, pozostały bez zmian.")
