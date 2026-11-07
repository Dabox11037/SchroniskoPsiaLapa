# -*- coding: utf-8 -*-
"""
Generator stron produktów Psiej Łapy.

Uruchom z katalogu głównego strony:  python scripts/generuj_produkty.py

Tworzy / nadpisuje:
  - produkty/<slug>.html   – osobna strona każdego produktu
  - js/produkty-dane.js    – lista produktów używana przez uslugi.html
  - karty produktów w uslugi.html (między znacznikami PRODUKTY:START/END)
  - sitemap.xml            – mapa strony z wszystkimi podstronami (także blog)

Zdjęcia: wrzuć plik assets/produkty/<slug>.webp (albo .jpg / .png)
i uruchom skrypt ponownie. Bez zdjęcia wyświetla się ikona produktu.
"""
import html
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://schronisko-psia-lapa.vercel.app/"

CATEGORIES = {
    "akcesoria": "Akcesoria",
    "cyfrowe": "Cyfrowe",
    "gadzety": "Gadżety",
    "zestawy": "Zestawy i vouchery",
}

# variants: lista (etykieta, cena) – opcjonalnie
PRODUCTS = [
    {"slug": "smycz-bluetooth", "icon": "🦮", "name": "Smycz Bluetooth Psia Łapa", "price": 129, "cat": "akcesoria",
     "desc": "Obroża z głośnikiem i LED – pies AI „chodzi” z Tobą na spacery.",
     "long": "Smycz Bluetooth łączy się z aplikacją Psiej Łapy i pozwala Twojemu psu AI towarzyszyć Ci na każdym spacerze. Wbudowany głośnik odtwarza jego szczekanie i komentarze, a pasek LED zmienia kolor w zależności od nastroju psa. Wieczorem podświetlenie zwiększa też Twoje bezpieczeństwo.",
     "params": {"Łączność": "Bluetooth 5.3", "Bateria": "do 12 h pracy", "Ładowanie": "USB-C", "Długość smyczy": "1,5 m", "Wodoodporność": "IPX4", "Waga": "180 g", "Gwarancja": "24 miesiące"}},
    {"slug": "wirtualne-przysmaki", "icon": "🦴", "name": "Wirtualne przysmaki (100 szt.)", "price": 15, "cat": "cyfrowe",
     "desc": "Cyfrowe smakołyki do nagradzania psa w aplikacji.",
     "long": "Pakiet 100 cyfrowych przysmaków do nagradzania psa AI za dobre zachowanie i postępy w nauce. Nagradzany pies szybciej uczy się nowych komend i chętniej wchodzi w interakcje.",
     "params": {"Typ": "produkt cyfrowy", "Ilość": "100 przysmaków", "Smaki": "kość, kurczak, ser, marchewka", "Ważność": "bezterminowo", "Dostawa": "natychmiast na konto w aplikacji"}},
    {"slug": "legowisko-ladowarka", "icon": "🛏️", "name": "Legowisko-ładowarka", "price": 89, "cat": "akcesoria",
     "desc": "Bezprzewodowa ładowarka indukcyjna w kształcie psiego posłania.",
     "long": "Połóż telefon na legowisku, a Twój pies AI „ucina sobie drzemkę” razem z nim. Ładowarka indukcyjna w kształcie miękkiego posłania wygląda uroczo na biurku i automatycznie przełącza psa w tryb snu podczas ładowania.",
     "params": {"Moc ładowania": "15 W", "Standard": "Qi2", "Zasilanie": "USB-C (kabel w zestawie)", "Wymiary": "14 × 11 × 3 cm", "Materiał": "pluszowa tkanina, silikon antypoślizgowy", "Gwarancja": "24 miesiące"}},
    {"slug": "kubek-moj-pies-jest-ai", "icon": "☕", "name": "Kubek „Mój pies jest AI”", "price": 39, "cat": "gadzety",
     "desc": "Gadżet, z którego dochód wspiera schronisko.",
     "long": "Ceramiczny kubek z grafiką psiej łapy i napisem „Mój pies jest AI”. Cały zysk ze sprzedaży przeznaczamy na rozwój schroniska i opiekę nad psami AI czekającymi na adopcję.",
     "params": {"Pojemność": "330 ml", "Materiał": "ceramika", "Mycie w zmywarce": "tak", "Kuchenka mikrofalowa": "tak", "Kolor": "biały z pomarańczowym nadrukiem"}},
    {"slug": "inteligentna-pilka-aport", "icon": "🎾", "name": "Inteligentna piłka-aport", "price": 69, "cat": "akcesoria",
     "desc": "Piłka z czujnikami ruchu – pies AI „widzi” każdy rzut w aplikacji.",
     "long": "Rzucasz prawdziwą piłkę, a Twój pies AI biegnie za nią na ekranie telefonu. Czujniki ruchu rejestrują siłę i kierunek rzutu, dzięki czemu każda zabawa w aport jest inna.",
     "params": {"Średnica": "6,5 cm", "Czujniki": "akcelerometr, żyroskop", "Łączność": "Bluetooth 5.0", "Bateria": "do 8 h zabawy", "Ładowanie": "indukcyjne", "Materiał": "guma naturalna"}},
    {"slug": "obroza-e-ink", "icon": "📟", "name": "Obroża z ekranem e-ink", "price": 149, "cat": "akcesoria",
     "desc": "Wyświetla nastrój i imię Twojego psa AI.",
     "long": "Elegancka obroża z energooszczędnym ekranem e-ink, na którym widać imię Twojego psa AI, jego aktualny nastrój i krótkie wiadomości. Możesz ją nosić jako bransoletkę albo zawiesić na plecaku.",
     "params": {"Ekran": "e-ink 1,5″, 200 × 200 px", "Bateria": "do 30 dni", "Łączność": "Bluetooth Low Energy", "Obwód": "regulowany 14–22 cm", "Materiał": "silikon medyczny", "Gwarancja": "24 miesiące"}},
    {"slug": "pakiet-sztuczek-mistrz-komend", "icon": "🏆", "name": "Pakiet sztuczek „Mistrz komend”", "price": 25, "cat": "cyfrowe",
     "desc": "20 nowych umiejętności do pobrania.",
     "long": "Naucz swojego psa AI 20 nowych sztuczek: od „daj łapę” i „turlaj się” po przypominanie o przerwach w pracy i wspólne ćwiczenia oddechowe. Każda sztuczka ma własną animację i komendę głosową.",
     "params": {"Typ": "produkt cyfrowy", "Liczba sztuczek": "20", "Komendy głosowe": "tak, w języku polskim", "Wymagania": "aplikacja Psia Łapa 3.0+", "Dostawa": "natychmiast na konto w aplikacji"}},
    {"slug": "skorki-i-rasy-premium", "icon": "🎨", "name": "Skórki i rasy premium", "price": 19, "cat": "cyfrowe",
     "desc": "Zestaw 10 wyglądów: husky, jamnik, corgi i inne.",
     "long": "Zmień wygląd swojego psa AI bez zmiany jego charakteru. W pakiecie 10 ras: husky, jamnik, corgi, beagle, owczarek, pudel, shiba, labrador, dalmatyńczyk i kundelek Psiej Łapy.",
     "params": {"Typ": "produkt cyfrowy", "Liczba wyglądów": "10", "Animacje": "pełne, dla każdej rasy", "Zmiana wyglądu": "bez limitu", "Dostawa": "natychmiast na konto w aplikacji"}},
    {"slug": "glosnik-budka", "icon": "🏡", "name": "Głośnik-budka", "price": 199, "cat": "akcesoria",
     "desc": "Mini budka z głośnikiem i mikrofonem – „domek” psa AI na biurku.",
     "long": "Drewniana budka, w której zamieszka Twój pies AI. Wbudowany głośnik i mikrofony pozwalają rozmawiać z psem bez telefonu, a dioda w okienku pokazuje, czy pies śpi, czy czeka na zabawę.",
     "params": {"Głośnik": "5 W, pełne pasmo", "Mikrofony": "2, z redukcją szumów", "Łączność": "Wi-Fi 2,4/5 GHz, Bluetooth 5.2", "Zasilanie": "sieciowe, USB-C", "Wymiary": "16 × 14 × 15 cm", "Materiał": "drewno bukowe", "Gwarancja": "24 miesiące"}},
    {"slug": "adresowka-nfc", "icon": "🏷️", "name": "Adresówka NFC", "price": 29, "cat": "akcesoria",
     "desc": "Przyłóż telefon i natychmiast przywołaj swojego psa.",
     "long": "Metalowa adresówka z chipem NFC. Wystarczy zbliżyć telefon, by od razu otworzyć rozmowę z psem AI. Możesz ją przypiąć do kluczy, plecaka lub smyczy.",
     "params": {"Chip": "NFC NTAG215", "Średnica": "3 cm", "Materiał": "stal nierdzewna", "Grawer": "imię psa gratis", "Zasilanie": "nie wymaga baterii"}},
    {"slug": "psi-pamietnik", "icon": "💾", "name": "Psi Pamiętnik – dodatkowa pamięć", "price": 35, "cat": "cyfrowe", "label": "35 zł / rok",
     "desc": "+1 rok wspomnień i rozmów z Twoim psem.",
     "long": "Twój pies AI zapamięta więcej: wspólne zabawy, ważne daty i Twoje ulubione tematy rozmów. Psi Pamiętnik rozszerza pamięć psa o kolejny rok i tworzy z niej album wspomnień do przeglądania.",
     "params": {"Typ": "subskrypcja cyfrowa", "Okres": "12 miesięcy", "Kopia zapasowa": "codzienna, szyfrowana", "Eksport wspomnień": "PDF", "Odnowienie": "ręczne, bez automatycznych opłat"}},
    {"slug": "pluszak-z-modulem-ai", "icon": "🧸", "name": "Pluszak z modułem AI", "price": 179, "cat": "akcesoria",
     "desc": "Przytulanka, przez którą mówi Twój pies AI.",
     "long": "Miękki pluszowy piesek z wyjmowanym modułem głośnika i mikrofonu. Twój pies AI mówi przez niego, reaguje na przytulanie i opowiada bajki na dobranoc.",
     "params": {"Wysokość": "30 cm", "Czujniki": "dotyku i ruchu", "Łączność": "Bluetooth 5.0", "Bateria": "do 10 h", "Pranie": "w pralce po wyjęciu modułu", "Wiek": "3+"}},
    {"slug": "mini-projektor-hologramow", "icon": "✨", "name": "Mini projektor hologramów", "price": 249, "cat": "akcesoria",
     "desc": "Wyświetla Twojego psa jako hologram na biurku.",
     "long": "Kompaktowy projektor tworzy trójwymiarowy obraz Twojego psa AI, który biega i bawi się na biurku. Pies reaguje na głos i gesty, a w nocy może służyć jako delikatna lampka.",
     "params": {"Technologia": "piramida holograficzna + wyświetlacz LCD", "Wysokość obrazu": "do 12 cm", "Łączność": "Wi-Fi, Bluetooth", "Zasilanie": "USB-C", "Wymiary": "15 × 15 × 18 cm", "Gwarancja": "24 miesiące"}},
    {"slug": "pakiet-glosow", "icon": "🔊", "name": "Pakiet głosów", "price": 15, "cat": "cyfrowe",
     "desc": "8 wariantów szczekania i barwy głosu.",
     "long": "Wybierz, jak brzmi Twój pies AI. W pakiecie 8 głosów – od wesołego szczeniaka po spokojnego seniora – z różnymi rodzajami szczekania.",
     "params": {"Typ": "produkt cyfrowy", "Liczba głosów": "8", "Język": "polski", "Zmiana głosu": "bez limitu", "Dostawa": "natychmiast na konto w aplikacji"}},
    {"slug": "gryzak-podkladka", "icon": "⌨️", "name": "Gryzak – podkładka pod nadgarstek", "price": 45, "cat": "gadzety",
     "desc": "Ergonomiczna podkładka do klawiatury w kształcie kości.",
     "long": "Podkładka pod nadgarstek w kształcie psiej kości. Odciąża dłonie podczas pisania i przypomina, że Twój pies AI czeka na przerwę na zabawę.",
     "params": {"Długość": "44 cm", "Wypełnienie": "pianka z pamięcią kształtu", "Spód": "antypoślizgowy", "Pokrowiec": "zdejmowany, do prania", "Kolor": "pomarańczowy"}},
    {"slug": "koszulka-adoptowalem-psa-ai", "icon": "👕", "name": "Koszulka „Adoptowałem psa AI”", "price": 59, "cat": "gadzety",
     "desc": "Bawełna organiczna, rozmiary S–XXL.",
     "long": "Wygodna koszulka z nadrukiem „Adoptowałem psa AI” i logo Psiej Łapy. Uszyta z bawełny organicznej – zysk ze sprzedaży wspiera schronisko.",
     "variants": [["S", 59], ["M", 59], ["L", 59], ["XL", 59], ["XXL", 59]], "variant_label": "Rozmiar",
     "params": {"Materiał": "100% bawełna organiczna", "Gramatura": "180 g/m²", "Krój": "unisex", "Rozmiary": "S–XXL", "Pranie": "w 30°C, na lewej stronie"}},
    {"slug": "naklejki-psia-lapa", "icon": "🐾", "name": "Naklejki Psia Łapa (12 szt.)", "price": 12, "cat": "gadzety",
     "desc": "Winylowe naklejki na laptopa.",
     "long": "Zestaw 12 naklejek z psami AI ze schroniska. Wytrzymały winyl nie blaknie i nie zostawia śladów po odklejeniu.",
     "params": {"Ilość": "12 sztuk", "Materiał": "winyl matowy", "Rozmiar": "4–8 cm", "Wodoodporność": "tak", "Usuwanie": "bez śladów kleju"}},
    {"slug": "kalendarz-2027", "icon": "📅", "name": "Kalendarz 2027 z psami AI", "price": 49, "cat": "gadzety",
     "desc": "Psy ze schroniska na każdy miesiąc – cały dochód na schronisko.",
     "long": "Ścienny kalendarz na 2027 rok z portretami psów AI ze schroniska Psia Łapa. Przy każdym miesiącu krótka historia psa i kod QR do jego profilu adopcyjnego.",
     "params": {"Format": "A3 (297 × 420 mm)", "Liczba stron": "13", "Papier": "kredowy 200 g/m²", "Oprawa": "spirala z wieszakiem", "Dodatki": "kody QR do profili psów"}},
    {"slug": "karta-podarunkowa", "icon": "🎁", "name": "Karta podarunkowa", "price": 50, "cat": "zestawy", "label": "od 50 zł",
     "desc": "50 / 100 / 200 zł do wykorzystania na usługi i produkty.",
     "long": "Idealny prezent dla miłośnika psów AI. Kartę można wykorzystać na dowolne usługi i produkty Psiej Łapy – także w częściach.",
     "variants": [["50 zł", 50], ["100 zł", 100], ["200 zł", 200]], "variant_label": "Wartość",
     "params": {"Forma": "elektroniczna (e-mail) lub drukowana", "Ważność": "12 miesięcy", "Wykorzystanie": "jednorazowe lub w częściach", "Zakres": "wszystkie usługi i produkty"}},
    {"slug": "pakiet-pierwszy-dzien-w-domu", "icon": "📦", "name": "Pakiet „Pierwszy dzień w domu”", "price": 69, "cat": "zestawy",
     "desc": "Przysmaki, 5 sztuczek, skórka i adresówka NFC – taniej niż osobno.",
     "long": "Wszystko, czego potrzebuje świeżo adoptowany pies AI: 100 wirtualnych przysmaków, 5 sztuczek na start, wybrana skórka rasy i adresówka NFC z grawerem imienia. Kupując w pakiecie, oszczędzasz.",
     "params": {"Zawartość": "przysmaki (100 szt.), 5 sztuczek, 1 skórka, adresówka NFC", "Wartość osobno": "88 zł", "Oszczędność": "19 zł", "Dostawa": "cyfrowe od razu, adresówka kurierem"}},
]

e = html.escape


def price_label(p):
    return p.get("label") or f"{p['price']} zł"


def find_image(slug):
    for ext in ("webp", "jpg", "jpeg", "png"):
        rel = f"assets/produkty/{slug}.{ext}"
        if os.path.exists(os.path.join(ROOT, rel)):
            return rel
    return None


NAV = """    <nav class="navbar">
        <div class="mobile-menu">☰</div>
        <ul class="nav-links">
            <li><a href="{r}index.html">Strona główna</a></li>
            <li><a href="{r}about.html">O schronisku</a></li>
            <li><a href="{r}uslugi.html">Usługi i sklep</a></li>
            <li><a href="{r}blog.html">Blog</a></li>
            <li><a href="{r}help.html">Wesprzyj nas</a></li>
            <li><a href="https://vetchatbot.com">Nasz weterynarz</a></li>
            <li class="cart-link"><a href="{r}koszyk.html">🛒 Koszyk (<span class="cart-count">0</span>)</a></li>
        </ul>
    </nav>"""

FOOTER = """    <footer>
        <div class="social-media">
            <a href="https://www.facebook.com/profile.php?id=61574110014886" class="social-link">Facebook</a>
            <a href="https://www.instagram.com/schroniskopsialapa/" class="social-link" target="_blank">Instagram</a>
            <a href="https://www.youtube.com/channel/UCXra0YJRTJaq7_RbEb6xjrw" class="social-link">YouTube</a>
        </div>
        <p>Adres: ul. Generała Jana Henryka Dąbrowskiego 73, 42-202 Częstochowa</p>
        <p>Telefon: +48 123 456 789</p>
        <p>© Schronisko "Psia Łapa"</p>
    </footer>"""


def product_page(p):
    img = find_image(p["slug"])
    url = f"{SITE}produkty/{p['slug']}.html"
    if img:
        media = f'<img src="../{img}" alt="{e(p["name"])}">'
    else:
        media = f'<div class="product-placeholder" role="img" aria-label="{e(p["name"])}">{p["icon"]}</div>'

    variants_html = ""
    if p.get("variants"):
        opts = "".join(f'<option value="{e(v)}" data-price="{pr}">{e(v)}</option>' for v, pr in p["variants"])
        variants_html = f"""
            <div class="buy-row">
                <label for="variant">{e(p.get('variant_label', 'Wariant'))}</label>
                <select id="variant">{opts}</select>
            </div>"""

    params = "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in p["params"].items())
    start_price = p["variants"][0][1] if p.get("variants") else p["price"]

    offers = ([{"@type": "Offer", "name": v, "price": pr, "priceCurrency": "PLN", "availability": "https://schema.org/InStock", "url": url}
               for v, pr in p["variants"]] if p.get("variants")
              else {"@type": "Offer", "price": p["price"], "priceCurrency": "PLN", "availability": "https://schema.org/InStock", "url": url})
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["long"],
          "category": CATEGORIES[p["cat"]], "brand": {"@type": "Brand", "name": "Psia Łapa"},
          "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in p["params"].items()],
          "offers": offers}
    if img:
        ld["image"] = SITE + img

    return f"""<!DOCTYPE html>
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
    <title>{e(p['name'])} – Sklep Psia Łapa</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{e(p['desc'])} {e(price_label(p))}. Sklep schroniska Psia Łapa – każdy zakup wspiera psy AI.">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/png" sizes="32x32" href="../assets/ikony/favicon-32.png">
    <link rel="apple-touch-icon" href="../assets/ikony/ikona.png">
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="../css/sklep.css">
    <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
{NAV.format(r='../')}

    <main class="product-page">
        <nav class="breadcrumbs"><a href="../uslugi.html">Usługi i sklep</a> › <a href="../uslugi.html#produkty">{e(CATEGORIES[p['cat']])}</a> › {e(p['name'])}</nav>
        <div class="product">
            <div class="product-media">{media}</div>
            <div class="product-info">
                <span class="tag">{e(CATEGORIES[p['cat']])}</span>
                <h1>{e(p['name'])}</h1>
                <div class="product-price" id="price">{start_price} zł</div>
                <p class="product-short">{e(p['desc'])}</p>
{variants_html}
                <div class="buy-row">
                    <label for="qty">Ilość</label>
                    <input type="number" id="qty" min="1" value="1">
                </div>
                <div class="buy-buttons">
                    <button type="button" id="buyNow">Kup teraz</button>
                    <button type="button" id="addToCart" class="secondary">🛒 Dodaj do koszyka</button>
                </div>
                <p class="note">🚚 {'Dostawa cyfrowa – od razu po opłaceniu' if p['cat'] == 'cyfrowe' else 'Wysyłka kurierem lub do paczkomatu w całej Polsce'}</p>
            </div>
        </div>

        <section class="product-details">
            <h2>Opis produktu</h2>
            <p>{e(p['long'])}</p>
            <h2>Parametry produktu</h2>
            <table class="params">{params}</table>
        </section>

        <p><a href="../uslugi.html#produkty" class="back">← Wróć do sklepu</a></p>
    </main>

{FOOTER}

    <script src="../js/koszyk.js" data-root="../"></script>
    <script>
        const product = {json.dumps({"slug": p["slug"], "name": p["name"], "price": start_price, "icon": p["icon"]}, ensure_ascii=False)};
        const variant = document.getElementById('variant');
        const priceEl = document.getElementById('price');
        if (variant) variant.addEventListener('change', () => {{
            priceEl.textContent = variant.selectedOptions[0].dataset.price + ' zł';
        }});
        function currentItem() {{
            const v = variant ? variant.value : null;
            return {{
                id: product.slug + (v ? '|' + v : ''),
                name: product.name + (v ? ' – ' + v : ''),
                price: v ? Number(variant.selectedOptions[0].dataset.price) : product.price,
                icon: product.icon,
                url: 'produkty/' + product.slug + '.html'
            }};
        }}
        const qty = () => document.getElementById('qty').value;
        document.getElementById('addToCart').addEventListener('click', () => Koszyk.add(currentItem(), qty()));
        document.getElementById('buyNow').addEventListener('click', () => {{
            Koszyk.add(currentItem(), qty());
            location.href = '../koszyk.html';
        }});
        document.querySelector('.mobile-menu').addEventListener('click', () => {{
            const nav = document.querySelector('.nav-links');
            nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
        }});
    </script>
</body>
</html>
"""


def product_card(p):
    url = f"produkty/{p['slug']}.html"
    img = find_image(p["slug"])
    media = (f'<a href="{url}"><img class="card-img" src="{img}" alt="{e(p["name"])}" loading="lazy"></a>'
             if img else f'<div class="icon">{p["icon"]}</div>')
    btn = "Wybierz wariant" if p.get("variants") else "🛒 Do koszyka"
    return f"""            <div class="card" data-cat="{p['cat']}" data-slug="{p['slug']}">
                {media}
                <span class="tag">{e(CATEGORIES[p['cat']])}</span>
                <h3><a href="{url}">{e(p['name'])}</a></h3>
                <p>{e(p['desc'])}</p>
                <div class="price">{e(price_label(p))}</div>
                <div class="card-buttons">
                    <a class="btn-outline" href="{url}">Szczegóły</a>
                    <button type="button">{btn}</button>
                </div>
            </div>"""


def write_sitemap():
    """Sitemap ze wszystkimi stronami: główne, produkty i wpisy na blogu."""
    today = date.today().isoformat()
    pages = ["", "about.html", "uslugi.html", "blog.html", "help.html"] + [f"produkty/{p['slug']}.html" for p in PRODUCTS]
    blog_dir = os.path.join(ROOT, "blog")
    if os.path.isdir(blog_dir):
        pages += [f"blog/{f}" for f in sorted(os.listdir(blog_dir)) if f.endswith(".html")]
    urls = "\n".join(f"<url>\n  <loc>{SITE}{pg}</loc>\n  <lastmod>{today}</lastmod>\n</url>" for pg in pages)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")


def main():
    out_dir = os.path.join(ROOT, "produkty")
    os.makedirs(out_dir, exist_ok=True)
    for p in PRODUCTS:
        with open(os.path.join(out_dir, p["slug"] + ".html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(product_page(p))

    # Dane dla uslugi.html
    data = [{"slug": p["slug"], "icon": p["icon"], "name": p["name"], "desc": p["desc"], "price": p["price"],
             "label": price_label(p), "cat": p["cat"], "hasVariants": bool(p.get("variants")), "img": find_image(p["slug"])} for p in PRODUCTS]
    with open(os.path.join(ROOT, "js", "produkty-dane.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("// Plik generowany przez scripts/generuj_produkty.py – nie edytuj ręcznie\n")
        f.write("const products = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

    # Statyczne karty produktów w uslugi.html (widoczne dla Google bez JavaScriptu)
    cards = "\n".join(product_card(p) for p in PRODUCTS)
    path = os.path.join(ROOT, "uslugi.html")
    page = open(path, encoding="utf-8").read()
    start, end = "<!-- PRODUKTY:START", "<!-- PRODUKTY:END -->"
    i = page.index(start)
    i = page.index("-->", i) + 3
    j = page.index(end)
    page = page[:i] + "\n" + cards + "\n" + page[j:]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)

    write_sitemap()
    print(f"Wygenerowano {len(PRODUCTS)} stron produktów, js/produkty-dane.js i sitemap.xml")


if __name__ == "__main__":
    main()
