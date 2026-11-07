# -*- coding: utf-8 -*-
"""
Generator bloga Psiej Łapy.

JAK DODAĆ WPIS
1. Utwórz plik w folderze  blog/wpisy/  np.  blog/wpisy/czym-jest-pies-ai.html
   Nazwa pliku (bez .html) = adres wpisu:  /blog/czym-jest-pies-ai.html
   Używaj małych liter, cyfr i myślników, bez polskich znaków.
2. Na początku pliku wpisz nagłówek z danymi wpisu, a pod nim treść w HTML:

    <!--
    tytul: Czym jest pies AI?
    opis: Krótki opis do Google i listy wpisów (1–2 zdania).
    data: 2026-11-07
    autor: Zespół Psiej Łapy
    obrazek: assets/blog/pies-ai.jpg
    -->
    <p>Treść wpisu...</p>
    <h2>Śródtytuł</h2>
    <p>...</p>

   Pola tytul, opis i data są wymagane; autor i obrazek – opcjonalne.
   Obrazki wrzucaj do assets/blog/ i podawaj ścieżkę od katalogu głównego
   (assets/blog/...) – skrypt sam poprawi ją dla strony wpisu.
3. Uruchom:   python scripts/generuj_bloga.py
4. Zrób commit i push – Vercel opublikuje wpis.

Aby usunąć wpis: skasuj plik z blog/wpisy/ i uruchom skrypt ponownie.

Skrypt tworzy / nadpisuje:  blog.html, blog/<slug>.html, sitemap.xml
"""
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generuj_produkty import ROOT, SITE, NAV, FOOTER, e, write_sitemap  # noqa: E402

SRC_DIR = os.path.join(ROOT, "blog", "wpisy")
OUT_DIR = os.path.join(ROOT, "blog")
MONTHS = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca",
          "sierpnia", "września", "października", "listopada", "grudnia"]

HEAD = """<!DOCTYPE html>
<html lang="pl">
<head>
<script src="https://web.cmp.usercentrics.eu/modules/autoblocker.js"></script>
<script id="usercentrics-cmp" src="https://web.cmp.usercentrics.eu/ui/loader.js" data-settings-id="EWT4dGICfkQ9Ib" async></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S20GPXQJT6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-S20GPXQJT6');
</script>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
{og_image}    <link rel="icon" type="image/png" sizes="32x32" href="{r}assets/ikony/favicon-32.png">
    <link rel="apple-touch-icon" href="{r}assets/ikony/ikona.png">
    <link rel="stylesheet" href="{r}css/main.css">
    <link rel="stylesheet" href="{r}css/blog.css">
{ld}</head>
<body>
{nav}
"""

TAIL = """
{footer}

    <script src="{r}js/koszyk.js" data-root="{r}"></script>
    <script>
        document.querySelector('.mobile-menu').addEventListener('click', () => {{
            const nav = document.querySelector('.nav-links');
            nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        }});
    </script>
</body>
</html>
"""


def pl_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MONTHS[m - 1]} {y}"


def clean_article(body):
    """Ujednolica wklejony HTML, żeby wygląd artykułu zależał tylko od css/blog.css.
    Plik źródłowy w blog/wpisy/ zostaje bez zmian – czyszczona jest tylko strona wynikowa."""
    # Stopka/uwaga pod artykułem (div z linią u góry, np. informacja o AI) -> klasa post-note
    body = re.sub(r'<div\b[^>]*style="[^"]*border-top[^"]*"[^>]*>', '<div class="post-note">', body, flags=re.I)
    # Wbudowane style, stare atrybuty wyglądu i znaczniki <font>/<center>
    body = re.sub(r'\s(style|align|bgcolor|color|face|border|cellpadding|cellspacing)\s*=\s*("[^"]*"|\'[^\']*\')', '', body, flags=re.I)
    body = re.sub(r'</?(font|center)\b[^>]*>', '', body, flags=re.I)
    # Strona ma już tytuł <h1> – nagłówki h1 z treści zamieniamy na h2
    body = re.sub(r'<(/?)h1\b', r'<\1h2', body, flags=re.I)
    # Tabele w przewijanym kontenerze (telefony)
    body = re.sub(r'<table\b', '<div class="table-wrap"><table', body, flags=re.I)
    body = re.sub(r'</table>', '</table></div>', body, flags=re.I)
    # Obrazki: leniwe ładowanie
    body = re.sub(r'<img\b(?![^>]*\bloading=)', '<img loading="lazy"', body, flags=re.I)
    return body


def parse(path):
    raw = open(path, encoding="utf-8").read().lstrip("﻿")
    m = re.match(r"\s*<!--(.*?)-->(.*)", raw, re.S)
    if not m:
        raise ValueError("brak nagłówka <!-- tytul: ... --> na początku pliku")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    for req in ("tytul", "opis", "data"):
        if not meta.get(req):
            raise ValueError(f"brak pola '{req}' w nagłówku")
    try:
        date.fromisoformat(meta["data"])
    except ValueError:
        raise ValueError(f"data '{meta['data']}' musi mieć format RRRR-MM-DD")
    slug = os.path.splitext(os.path.basename(path))[0]
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        raise ValueError("nazwa pliku może zawierać tylko małe litery, cyfry i myślniki")
    body = m.group(2).strip()
    # Ścieżki od katalogu głównego (assets/...) -> względne dla /blog/
    body = re.sub(r'(src|href)="(assets/|produkty/|[a-z0-9-]+\.html)', r'\1="../\2', body)
    body = clean_article(body)
    return {"slug": slug, "title": meta["tytul"], "desc": meta["opis"], "date": meta["data"],
            "author": meta.get("autor", "Zespół Psiej Łapy"), "image": meta.get("obrazek"), "body": body}


def post_page(p):
    url = f"{SITE}blog/{p['slug']}.html"
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
          "description": p["desc"], "datePublished": p["date"], "url": url,
          "author": {"@type": "Organization", "name": p["author"]},
          "publisher": {"@type": "Organization", "name": "Schronisko dla Psów Psia Łapa"}}
    og_image = ""
    cover = ""
    if p["image"]:
        ld["image"] = SITE + p["image"]
        og_image = f'    <meta property="og:image" content="{SITE}{e(p["image"])}">\n'
        cover = f'<img class="post-cover" src="../{e(p["image"])}" alt="{e(p["title"])}">'
    head = HEAD.format(title=e(p["title"]) + " – Blog Psia Łapa", desc=e(p["desc"]), url=url, og_type="article",
                       og_image=og_image, r="../", nav=NAV.format(r="../"),
                       ld=f'    <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    return head + f"""
    <main class="blog-page">
        <nav class="breadcrumbs"><a href="../blog.html">Blog</a> › {e(p['title'])}</nav>
        <article class="post">
            <h1>{e(p['title'])}</h1>
            <p class="post-meta">{pl_date(p['date'])} · {e(p['author'])}</p>
            {cover}
            <div class="post-body">
{p['body']}
            </div>
        </article>
        <p><a href="../blog.html" class="back">← Wszystkie wpisy</a></p>
    </main>
""" + TAIL.format(footer=FOOTER, r="../")


def index_page(posts):
    items = []
    for p in posts:
        img = (f'<a href="blog/{p["slug"]}.html"><img src="{e(p["image"])}" alt="{e(p["title"])}" loading="lazy"></a>'
               if p["image"] else "")
        items.append(f"""            <article class="post-card">
                {img}
                <div class="post-card-body">
                    <p class="post-meta">{pl_date(p['date'])}</p>
                    <h2><a href="blog/{p['slug']}.html">{e(p['title'])}</a></h2>
                    <p>{e(p['desc'])}</p>
                    <a class="more" href="blog/{p['slug']}.html">Czytaj dalej →</a>
                </div>
            </article>""")
    listing = "\n".join(items) or '            <p class="empty">Wkrótce pojawią się tu pierwsze wpisy 🐾</p>'
    head = HEAD.format(title="Blog – Psia Łapa, schronisko dla psów AI",
                       desc="Blog schroniska Psia Łapa: porady, ciekawostki i historie o psach sztucznej inteligencji.",
                       url=f"{SITE}blog.html", og_type="website", og_image="", r="", nav=NAV.format(r=""), ld="")
    return head + f"""
    <header class="hero">
        <h1>Blog Psiej Łapy</h1>
        <p>Porady, ciekawostki i historie o psach sztucznej inteligencji</p>
    </header>

    <main class="blog-page">
        <div class="post-list">
{listing}
        </div>
    </main>
""" + TAIL.format(footer=FOOTER, r="")


def main():
    os.makedirs(SRC_DIR, exist_ok=True)
    posts, errors = [], []
    for f in sorted(os.listdir(SRC_DIR)):
        if not f.endswith(".html"):
            continue
        try:
            posts.append(parse(os.path.join(SRC_DIR, f)))
        except ValueError as err:
            errors.append(f"  ✗ {f}: {err}")
    if errors:
        print("Błędy we wpisach (nic nie zostało zmienione):\n" + "\n".join(errors))
        sys.exit(1)

    posts.sort(key=lambda p: p["date"], reverse=True)

    # Usuń strony wpisów, których plik źródłowy skasowano
    keep = {p["slug"] + ".html" for p in posts}
    for f in os.listdir(OUT_DIR):
        if f.endswith(".html") and f not in keep:
            os.remove(os.path.join(OUT_DIR, f))

    for p in posts:
        with open(os.path.join(OUT_DIR, p["slug"] + ".html"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(post_page(p))
    with open(os.path.join(ROOT, "blog.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(index_page(posts))
    write_sitemap()
    print(f"Wygenerowano blog: {len(posts)} wpis(ów), blog.html i sitemap.xml")


if __name__ == "__main__":
    main()
