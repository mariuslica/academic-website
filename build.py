# -*- coding: utf-8 -*-
"""
Generator pentru site-ul academic.

CUM SE FOLOSEȘTE
1. Modifici textele din secțiunea DATE PERSONALE de mai jos.
   Tot ce e marcat cu [DE COMPLETAT] trebuie înlocuit (sau șters).
2. Rulezi:  python build.py
3. Site-ul gata făcut apare în folderul docs/ – acela se publică pe GitHub Pages.
Nu are nevoie de pachete suplimentare, doar Python 3.
"""
from pathlib import Path
import html, json, shutil

# =====================================================================
# DATE PERSONALE – modifică aici
# =====================================================================
NUME = "Marius Lică"
INITIALE = "ML"
SUBTITLU = "Cercetare & profil academic"
POZITIE = "Doctorand · Școala Doctorală de Inginerie Electrică"
EMAIL = ""        # ex. "nume@upb.ro" – dacă e gol, nu apare pe site
ORCID = "0009-0000-3341-0688"        # ex. "0000-0002-1234-5678"
SCOPUS = ""
LINKEDIN = ""
GOOGLE_SCHOLAR = ""
GITHUB = "https://github.com/mariuslica"
AN = "2026"

LEAD = ("Deep learning pentru clasificarea organitelor subcelulare în microscopia de fluorescență. "
        "Doctorand la Școala Doctorală de Inginerie Electrică, Universitatea Națională de Știință și Tehnologie "
        "POLITEHNICA București.")

METRICI = [
    ("9", "Clase de organite subcelulare"),
    ("5-fold", "Validare încrucișată stratificată"),
    ("MobileNetV2", "Transfer learning"),
    ("Cascadă", "Arhitectură de clasificatori"),
]

TEME = [
    ("01 / DEEP LEARNING", "Rețele neuronale convoluționale",
     "Transfer learning cu modele preantrenate, adaptate la imagini biomedicale cu seturi de date limitate."),
    ("02 / MICROSCOPIE", "Imagini de fluorescență",
     "Recunoașterea automată a organitelor subcelulare și analiza particularităților imaginilor de fluorescență."),
    ("03 / FIABILITATE", "Predicții de încredere",
     "Praguri de încredere cu opțiune de respingere și clasificatori în cascadă pentru clasele greu de separat."),
]

ETAPE_CERCETARE = [
    ("Etapa curentă", "Transfer learning și clasificare în cascadă",
     "Clasificarea a 9 clase de organite cu MobileNetV2 preantrenat, validare încrucișată stratificată 5-fold, prag de încredere "
     "cu opțiune de respingere și arhitectură de clasificatori în cascadă. Transferul de învățare a dublat aproape acuratețea "
     "față de CNN-ul de bază; cele mai mari câștiguri pe clasă au apărut la Golgi și ADN."),
    ("Etape anterioare", "Model de bază și pregătirea datelor",
     "Organizarea setului de imagini pe seturi de antrenare și testare și construirea unei rețele convoluționale de referință."),
]

PUBLICATII = [
    # Exemplu de adăugat când ai o lucrare publicată (șterge # din fața rândurilor):
    # ("2027", "Conferințe internaționale",
    #  "Autori, „Titlul articolului”, Numele conferinței, pp. x–y, 2027.",
    #  "10.xxxx/xxxxx"),
]

EXPERIENTA = []   # lasă gol ca să nu apară secțiunea

EDUCATIE = [
    ("În curs", "Doctorand în Inginerie Electrică",
     "Școala Doctorală de Inginerie Electrică, Universitatea Națională de Știință și Tehnologie POLITEHNICA București. "
     "Tema: deep learning pentru clasificarea organitelor subcelulare în microscopia de fluorescență."),
]

COMPETENTE = ("Python, TensorFlow/Keras, Jupyter; rețele neuronale convoluționale, transfer learning, "
              "validare încrucișată stratificată; prelucrarea și analiza imaginilor de microscopie.")

DESPRE = ("Sunt doctorand la Școala Doctorală de Inginerie Electrică a Universității POLITEHNICA din București. "
          "Cercetarea mea folosește învățarea profundă pentru a recunoaște automat organitele subcelulare în imagini "
          "de microscopie de fluorescență, cu accent pe predicții fiabile: modelul trebuie să știe și când nu este sigur.")

# =====================================================================
# De aici în jos nu trebuie modificat nimic
# =====================================================================
root = Path(__file__).resolve().parent
src, out = root / "source", root / "docs"
esc = html.escape
out.mkdir(exist_ok=True)
shutil.copy(src / "styles.css", out / "styles.css")
shutil.copy(src / "app.js", out / "app.js")
(out / ".nojekyll").write_text("")
with (out / "styles.css").open("a", encoding="utf-8") as f:
    f.write("\n.citation{margin:10px 0;overflow-wrap:anywhere}.section>h2{margin-top:45px}.hero-portrait{max-width:300px;justify-self:end}.nav{gap:20px}"
            ".placeholder-portrait{aspect-ratio:1;display:grid;place-items:center;font:96px var(--serif);color:var(--accent)}"
            "@media print{.header,.footer,button{display:none!important}.wrap{width:100%}}")

# Poza: pune un fișier source/portrait.jpg; altfel se afișează inițialele
has_photo = (src / "portrait.jpg").exists()
if has_photo:
    shutil.copy(src / "portrait.jpg", out / "portrait.jpg")
portrait = (f'<img src="portrait.jpg" width="368" height="368" alt="{esc(NUME)}">' if has_photo
            else f'<div class="placeholder-portrait" aria-hidden="true">{esc(INITIALE)}</div>')

links = [("ORCID", f"https://orcid.org/{ORCID}" if ORCID else ""),
         ("Scopus", f"https://www.scopus.com/authid/detail.uri?authorId={SCOPUS}" if SCOPUS else ""),
         ("Google Scholar", GOOGLE_SCHOLAR), ("LinkedIn", LINKEDIN), ("GitHub", GITHUB)]
profiles = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n} ↗</a>' for n, u in links if u)

nav = [("index", "Acasă"), ("research", "Cercetare"), ("publications", "Publicații"), ("about", "Profil"), ("contact", "Contact")]


def page(key, title, body):
    menu = "".join(f'<a href="{k}.html"' + (' aria-current="page"' if k == key else "") + f">{v}</a>" for k, v in nav)
    doc = f'''<!doctype html><html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow"><title>{title} | {esc(NUME)}</title>
<meta name="description" content="Profilul academic al lui {esc(NUME)}: cercetare doctorală în inginerie electrică, publicații și experiență profesională.">
<link rel="stylesheet" href="styles.css"><script defer src="app.js"></script></head><body>
<a class="skip" href="#main">Salt la conținut</a>
<header class="header"><div class="wrap header-inner"><a class="brand" href="index.html"><span class="monogram">{esc(INITIALE)}</span><span class="brand-name">{esc(NUME)}<small>{esc(SUBTITLU)}</small></span></a>
<button class="menu-toggle" aria-expanded="false" aria-controls="navigation">Meniu</button><nav id="navigation" class="nav" aria-label="Navigare principală">{menu}</nav></div></header>
<main id="main">{body}</main>
<footer class="footer"><div class="wrap"><div class="footer-top"><div><strong>{esc(NUME)}</strong><br>Inginerie electrică · POLITEHNICA București</div><nav aria-label="Profiluri academice">{profiles}<a href="about.html">Profil</a></nav></div>
<div class="footer-bottom"><span>© {AN} {esc(NUME)} · București, România</span></div></div></footer></body></html>'''
    (out / f"{key}.html").write_text(doc, encoding="utf-8")


def intro(title, desc, tag="Profil academic"):
    return f'<div class="wrap page-intro"><p class="eyebrow">{tag}</p><h1>{title}</h1><p class="lead">{desc}</p></div>'


def rows(items):
    return "".join(f'<article class="timeline-row"><div class="date">{esc(a)}</div><div><h3>{esc(b)}</h3><p>{esc(c)}</p></div></article>' for a, b, c in items)


def pubrow(p):
    an, cat, text, doi = p
    link = f'<a href="{doi if doi.startswith("http") else "https://doi.org/" + doi}" target="_blank" rel="noopener">DOI / Editor ↗</a>' if doi else ""
    return (f'<article class="pub-row" data-search="{esc(text, quote=True)}" data-year="{an}" data-type="{esc(cat, quote=True)}">'
            f'<div class="pub-year">{an}</div><div><div class="pub-meta">{esc(cat)}</div><p class="citation">{esc(text)}</p><div class="pub-actions">{link}</div></div></article>')


teme_html = '<div class="themes">' + "".join(
    f'<article class="theme"><span class="num">{a}</span><h3>{b}</h3><p>{c}</p><a href="research.html">Direcții de cercetare →</a></article>' for a, b, c in TEME) + "</div>"
FARA_PUB = '<p class="lead">Lucrări în pregătire. Lista va fi actualizată pe măsură ce articolele sunt publicate.</p>'
nume_h1 = esc(NUME).replace(" ", "<br>", 1)

# ---- Acasă
page("index", "Acasă", f'''<div class="wrap"><section class="hero"><div><p class="eyebrow">Inginerie electrică · Deep learning · Analiza imaginilor</p>
<h1>{nume_h1}</h1><p class="position">{esc(POZITIE)}</p><p class="lead">{esc(LEAD)}</p>
<div class="buttons"><a class="button" href="research.html">Explorează cercetarea →</a><a class="button secondary" href="publications.html">Vezi publicațiile</a></div>
<div class="profile-links">{profiles}</div></div>
<div class="hero-portrait"><figure>{portrait}<figcaption class="portrait-caption"><span>UNSTPB · București</span></figcaption></figure></div></section>
<div class="metrics">{"".join(f'<div class="metric"><strong>{esc(a)}</strong><span>{esc(b)}</span></div>' for a, b in METRICI)}</div></div>
<section class="section wrap"><div class="section-head"><div><p class="eyebrow">Domenii de interes</p><h2>De la imagine la decizie.</h2></div></div>{teme_html}</section>
<section class="section wrap"><div class="section-head"><div><p class="eyebrow">Lucrări selectate</p><h2>Publicații și contribuții</h2></div><a class="text-link" href="publications.html">Toate publicațiile →</a></div>
<div class="pub-list">{"".join(pubrow(p) for p in PUBLICATII[:3]) or FARA_PUB}</div></section>
<section class="wrap section"><div class="callout"><div><p class="eyebrow">Colaborare</p><h2>Inteligență artificială pentru imagini biomedicale.</h2><p>Deschis la colaborări în analiza imaginilor de microscopie și învățare profundă.</p></div><div class="buttons"><a href="contact.html" class="button secondary">Contact</a></div></div></section>''')

# ---- Cercetare
page("research", "Cercetare", intro("Cercetare", "Învățare profundă pentru clasificarea organitelor subcelulare în microscopia de fluorescență.", "Teza de doctorat")
     + f'''<section class="section wrap"><div class="prose"><h2>Tema tezei</h2><p>Localizarea proteinelor în organitele celulei spune mult despre funcția lor. Teza dezvoltă modele de rețele neuronale
convoluționale care recunosc automat organitul dintr-o imagine de microscopie de fluorescență, cu accent pe fiabilitate: estimarea încrederii,
respingerea predicțiilor nesigure și arhitecturi în cascadă pentru clasele greu de separat.</p></div>
<h2>Etapele cercetării</h2>{rows(ETAPE_CERCETARE)}</section>
<section class="section wrap"><div class="section-head"><div><p class="eyebrow">Domenii de interes</p><h2>Direcții de lucru</h2></div></div>{teme_html}</section>''')

# ---- Publicații
ani = sorted({p[0] for p in PUBLICATII}, reverse=True)
cats = list(dict.fromkeys(p[1] for p in PUBLICATII))
opt = lambda v: "".join(f"<option>{esc(x)}</option>" for x in v)
(out / "publications.json").write_text(json.dumps([dict(zip(["an", "categorie", "referinta", "doi"], p)) for p in PUBLICATII], ensure_ascii=False, indent=2), encoding="utf-8")
page("publications", "Publicații", intro("Publicații", "Articole și contribuții științifice în învățare profundă și analiza imaginilor.")
     + f'''<section class="wrap section"><form class="filters" data-filter-form><label class="search-field">Caută după titlu, autor sau cuvânt-cheie<input type="search" placeholder="De exemplu: deep learning, organite"></label>
<label>An<select name="year"><option value="">Toți anii</option>{opt(ani)}</select></label><label>Categorie<select name="type"><option value="">Toate categoriile</option>{opt(cats)}</select></label>
<button type="button" class="button secondary" data-reset>Resetează</button></form>
<div class="filter-count"><span data-result-count aria-live="polite">{len(PUBLICATII)} lucrări</span><a href="publications.json" download>Descarcă datele (JSON)</a></div>
<div class="pub-list">{"".join(pubrow(p) for p in PUBLICATII) or FARA_PUB}</div><p class="empty" data-empty hidden>Nicio lucrare nu corespunde filtrelor.</p></section>''')

# ---- Profil
page("about", "Profil", intro("Profil", esc(POZITIE))
     + f'''<section class="section wrap"><div class="prose"><h2>Despre mine</h2><p>{esc(DESPRE)}</p></div>
{("<h2>Experiență profesională</h2>"+rows(EXPERIENTA)) if EXPERIENTA else ""}<h2>Educație și formare</h2>{rows(EDUCATIE)}
<div class="prose"><h2>Competențe</h2><p>{esc(COMPETENTE)}</p></div>
<button class="button secondary" data-print>Tipărește / Salvează PDF</button></section>''')

# ---- Contact
EMAIL_CARD = f'<article class="contact-card"><h2>E-mail</h2><a href="mailto:{EMAIL}">{esc(EMAIL)}</a></article>' if EMAIL else ""
ids = "".join(f"{n}: <a href=\"{u}\">{u}</a><br>" for n, u in links if u) or "—"
page("contact", "Contact", intro("Să colaborăm.", "Pentru colaborări de cercetare și discuții despre învățare profundă și analiza imaginilor biomedicale.")
     + f'''<section class="section wrap contact-grid"><div>{EMAIL_CARD}
<article class="contact-card"><h2>Afiliere</h2><p>Școala Doctorală de Inginerie Electrică<br>Universitatea Națională de Știință și Tehnologie POLITEHNICA București</p><p>Splaiul Independenței nr. 313<br>060042, București, România</p></article></div>
<div><article class="contact-card"><h2>Identificatori academici</h2><p>{ids}</p></article></div></section>''')

print("Gata. Site generat în folderul docs/")
