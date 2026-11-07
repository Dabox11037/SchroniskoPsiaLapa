# Schronisko Psia Łapa – instrukcja obsługi strony

Strona: https://schronisko-psia-lapa.vercel.app/
Hosting: Vercel – każdy `git push` na gałąź `main` automatycznie publikuje stronę.

Spis treści:
1. [Przygotowanie komputera (raz)](#1-przygotowanie-komputera-raz)
2. [Jak uruchomić skrypt](#2-jak-uruchomić-skrypt)
3. [Dodawanie artykułu na blog](#3-dodawanie-artykułu-na-blog)
4. [Edycja i usuwanie artykułów](#4-edycja-i-usuwanie-artykułów)
5. [Produkty w sklepie](#5-produkty-w-sklepie)
6. [Publikacja zmian](#6-publikacja-zmian)
7. [Co robi każdy skrypt](#7-co-robi-każdy-skrypt)
8. [Najczęstsze problemy](#8-najczęstsze-problemy)
9. [Struktura plików](#9-struktura-plików)

---

## 1. Przygotowanie komputera (raz)

Potrzebny jest **Python 3** i biblioteka **Pillow** (do zdjęć).

Sprawdź w terminalu:

```
python --version
```

Jeśli pokazuje wersję (np. `Python 3.12.1`) – Python jest. Jeśli nie – pobierz go z https://www.python.org/downloads/ i przy instalacji zaznacz **„Add Python to PATH”**.

Zainstaluj Pillow:

```
pip install pillow
```

---

## 2. Jak uruchomić skrypt

1. Otwórz folder strony w **VS Code**.
2. Otwórz terminal: menu **Terminal → New Terminal** (albo skrót <kbd>Ctrl</kbd> + <kbd>`</kbd>).
   Terminal otworzy się już w folderze strony (`...\SchroniskoPsiaLapa>`).
3. Wpisz polecenie i naciśnij <kbd>Enter</kbd>, np.:

```
python scripts/przygotuj_wpisy.py
```

> Polecenia uruchamiaj zawsze z **głównego folderu strony** (tam, gdzie jest `index.html`).
> Jeśli terminal jest w innym miejscu, przejdź do folderu strony:
> `cd C:\Users\kompik\Desktop\strona\SchroniskoPsiaLapa`

Działający skrypt można w każdej chwili przerwać: <kbd>Ctrl</kbd> + <kbd>C</kbd>.

---

## 3. Dodawanie artykułu na blog

### Krok 1 – wrzuć plik z artykułem

Skopiuj plik `.html` z treścią artykułu do folderu:

```
blog/wpisy/
```

Nazwa pliku może być dowolna (np. `Wyprawka_dla_psa_AI.html`) – skrypt ją poprawi.
Plik ma zawierać **samą treść** (`<p>`, `<h2>`, `<img>` …), bez `<html>`, `<head>`, `<body>` i bez tytułu `<h1>` – tytuł dodaje strona.

Okładkę (jpg/png) możesz trzymać gdziekolwiek, np. w Pobranych – skrypt sam ją skopiuje i przekonwertuje.

### Krok 2 – uruchom skrypt

```
python scripts/przygotuj_wpisy.py
```

Skrypt zapyta po kolei o dane artykułu. W nawiasie `[ ]` pokazuje **podpowiedź** – <kbd>Enter</kbd> ją akceptuje, a jeśli coś wpiszesz, zastąpisz podpowiedź.

| Pytanie | Co wpisać | Wskazówka |
|---|---|---|
| **Tytuł artykułu** | pełny tytuł z polskimi znakami | Podpowiedź jest z nazwy pliku, bez polskich znaków – lepiej wpisać ręcznie. |
| **Opis** | 1–2 zdania, ok. 150 znaków | Pokazuje się w Google i na liście wpisów. Napisz własne zdanie zachęcające do czytania. |
| **Data publikacji** | `RRRR-MM-DD`, np. `2026-11-10` | Enter = dzisiaj. Wpisy na blogu są sortowane od najnowszych. |
| **Autor** | np. `Zespół Psiej Łapy` | |
| **Adres wpisu** | małe litery, cyfry, myślniki | Tworzy się z tytułu. Jeśli jest długi albo kończy się dziwnie – wpisz krótszy, np. `wyprawka-dla-psa-ai`. Artykuł będzie pod adresem `/blog/wyprawka-dla-psa-ai.html`. |
| **Obrazek okładki** | **przeciągnij plik jpg do terminala** albo wklej ścieżkę | Skrypt zamieni go na WebP i zapisze jako `assets/blog/<adres-wpisu>.webp`. Enter = pierwsze zdjęcie z artykułu, `-` = bez okładki. |
| **Tekst alt** (dla każdego zdjęcia) | krótki opis tego, co widać na zdjęciu | Ważne dla Google Grafika i osób niewidomych. `-` = zdjęcie czysto dekoracyjne. |

Przykład:

```
[1/1] Wyprawka_dla_psa_AI.html
  Początek: Listopad przynosi ze sobą wyraźne ochłodzenie…

  Tytuł artykułu [Wyprawka dla psa AI]: Wyprawka dla psa AI na start – jakie akcesoria wybrać?
  Opis (do Google, ok. 150 znaków) [Listopad przynosi…]: Sprawdź, jakie akcesoria przydadzą się psu AI na spacery i na co dzień.
  Data publikacji (RRRR-MM-DD) [2026-11-07]:
  Autor [Zespół Psiej Łapy]:
  Adres wpisu (nazwa pliku) [wyprawka-dla-psa-ai-na-start-jakie-akcesoria-wybrac]: wyprawka-dla-psa-ai
  Okładka: przeciągnij plik (jpg/png/webp) do terminala albo wklej ścieżkę.
  Obrazek okładki (Enter = podpowiedź, '-' = brak) [...]: & "C:\Users\kompik\Downloads\okladka.jpg"
  ✓ Okładka przekonwertowana do WebP: assets/blog/wyprawka-dla-psa-ai.webp (2400 KB → 180 KB)

  Zdjęcie 1/3: https://schronisko-psia-lapa.vercel.app/assets/produkty/smycz-bluetooth.webp
  Tekst alt [Smycz Bluetooth Psia Łapa]: Smycz Bluetooth ze świecącym paskiem LED
  ...
  ✓ Zapisano jako blog/wpisy/wyprawka-dla-psa-ai.html

Generuję blog…
Wygenerowano blog: 3 wpis(ów), blog.html i sitemap.xml
```

Na końcu skrypt **sam generuje blog** – nie trzeba uruchamiać nic więcej.

### Krok 3 – sprawdź i opublikuj

Otwórz `blog.html` w przeglądarce (dwuklik w Eksploratorze plików), sprawdź wpis, a potem opublikuj zmiany – patrz [punkt 6](#6-publikacja-zmian).

### Zdjęcia wewnątrz artykułu

- Zdjęcia z naszej strony (np. `https://schronisko-psia-lapa.vercel.app/assets/produkty/...`) działają od razu.
- Własne zdjęcia wrzuć do `assets/blog/` i w artykule podaj ścieżkę **od głównego folderu strony**:
  `<img src="assets/blog/moje-zdjecie.webp" alt="Opis zdjęcia">` – skrypt sam poprawi ją dla strony wpisu.
- Linki do innych podstron też podawaj od głównego folderu, np. `<a href="uslugi.html">`.

---

## 4. Edycja i usuwanie artykułów

**Poprawka treści albo danych** – otwórz plik w `blog/wpisy/`, zmień to, co trzeba (treść albo pola w nagłówku na górze pliku), zapisz i uruchom:

```
python scripts/generuj_bloga.py
```

Nagłówek przygotowanego wpisu wygląda tak:

```html
<!--
tytul: Wyprawka dla psa AI na start – jakie akcesoria wybrać?
opis: Sprawdź, jakie akcesoria przydadzą się psu AI na spacery i na co dzień.
data: 2026-11-07
autor: Zespół Psiej Łapy
obrazek: assets/blog/wyprawka-dla-psa-ai.webp
-->
```

**Usunięcie wpisu** – skasuj jego plik z `blog/wpisy/` i uruchom `python scripts/generuj_bloga.py`. Strona wpisu zniknie z bloga i z mapy strony.

> Nie edytuj plików w folderze `blog/` (poza `blog/wpisy/`) ani `blog.html` – są tworzone przez skrypt i każda ręczna zmiana zostanie nadpisana.

---

## 5. Produkty w sklepie

Wszystkie produkty (nazwa, cena, opis, parametry, warianty) są w pliku:

```
scripts/generuj_produkty.py
```

na liście `PRODUCTS`. Po każdej zmianie uruchom:

```
python scripts/generuj_produkty.py
```

**Zdjęcie produktu** – zapisz plik jako `assets/produkty/<adres-produktu>.webp` (albo `.jpg` / `.png`), np. `assets/produkty/smycz-bluetooth.webp`, i uruchom skrypt. Adres produktu to pole `slug` na liście.

**Nowy produkt** – skopiuj w pliku jeden blok `{ "slug": ..., ... },`, zmień dane i uruchom skrypt. Kategorie (`cat`): `akcesoria`, `cyfrowe`, `gadzety`, `zestawy`.

> Nie edytuj ręcznie plików w `produkty/`, `produkty-dane.js` ani kart produktów w `uslugi.html` – są tworzone przez skrypt.

---

## 6. Publikacja zmian

W terminalu:

```
git add .
git commit -m "Nowy wpis na blogu: wyprawka dla psa AI"
git push
```

albo w VS Code: zakładka **Source Control** (ikona rozgałęzienia po lewej) → wpisz opis → **Commit** → **Sync Changes**.

Po 1–2 minutach Vercel opublikuje zmiany.

**Żeby Google szybciej znalazło nowy wpis:** w [Google Search Console](https://search.google.com/search-console) wklej adres wpisu w „Sprawdzanie adresu URL” i kliknij **„Poproś o zindeksowanie”**.

---

## 7. Co robi każdy skrypt

| Polecenie | Kiedy używać | Co robi |
|---|---|---|
| `python scripts/przygotuj_wpisy.py` | dodajesz **nowy artykuł** | Pyta o dane, dopisuje nagłówek, zmienia nazwę pliku, konwertuje okładkę do WebP, uzupełnia teksty alt (także brakujące w starych wpisach), generuje blog. |
| `python scripts/generuj_bloga.py` | **poprawiłaś** albo **usunęłaś** wpis | Tworzy `blog.html`, strony wpisów w `blog/` i mapę strony. |
| `python scripts/generuj_produkty.py` | zmiana **produktów** albo ich zdjęć | Tworzy strony w `produkty/`, karty w `uslugi.html`, `produkty-dane.js` i mapę strony. |

Wszystkie skrypty aktualizują `sitemap.xml` – zawsze zawiera komplet stron.

---

## 8. Najczęstsze problemy

| Komunikat / problem | Rozwiązanie |
|---|---|
| `python` nie jest rozpoznawany | Zainstaluj Pythona (punkt 1) z opcją „Add Python to PATH” i otwórz terminal ponownie. Możesz też spróbować `py` zamiast `python`. |
| `can't open file ... scripts/...` | Terminal jest w złym folderze – przejdź do folderu strony (`cd ...\SchroniskoPsiaLapa`). |
| `Brak biblioteki Pillow` | `pip install pillow` |
| `Błędy we wpisach (nic nie zostało zmienione)` | Któryś plik w `blog/wpisy/` nie ma nagłówka albo ma błąd (np. zła data). Uruchom `python scripts/przygotuj_wpisy.py` albo popraw nagłówek według komunikatu. |
| `Nie ma pliku ...` przy okładce | Przeciągnij plik do terminala jeszcze raz albo wklej pełną ścieżkę. |
| `Plik ... już istnieje – pomijam` | Wpis o takim adresie już jest – uruchom skrypt ponownie i podaj inny adres. |
| Krzaki zamiast polskich liter w terminalu | Wpisz najpierw `chcp 65001`, potem uruchom skrypt. |

---

## 9. Struktura plików

```
index.html, about.html, help.html   – strony główne (edycja ręczna)
uslugi.html                         – usługi i sklep (karty produktów wstawia skrypt)
koszyk.html, koszyk.js              – koszyk
sklep.css, blog.css                 – style sklepu i bloga
blog.html                           – lista wpisów         (generowane)
blog/*.html                         – strony wpisów        (generowane)
blog/wpisy/*.html                   – ARTYKUŁY – tu wrzucasz pliki
produkty/*.html                     – strony produktów     (generowane)
produkty-dane.js                    – dane produktów       (generowane)
assets/produkty/                    – zdjęcia produktów
assets/blog/                        – okładki i zdjęcia do artykułów
scripts/                            – skrypty
sitemap.xml                         – mapa strony          (generowane)
robots.txt                          – zasady dla robotów wyszukiwarek
```
