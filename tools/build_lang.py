"""Genera /en/, /es/ y /de/ a partir de index.html y su diccionario I18N.
Ejecutar tras cada cambio de index.html:  python tools/build_lang.py"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://pizzeriakebabnumero1.it/"
META = {
    "en": {
        "locale": "en_GB",
        "title": "Takeaway pizza & kebab in Como · Numero 1, wood-fired oven",
        "desc": "Numero 1 takeaway pizzeria and kebab in Monte Olimpino, Como, with a wood-fired oven. Any pizza €5.99, drink +€1. Open every day 6 pm to 11 pm.",
        "og_title": "Takeaway pizza & kebab in Como · Numero 1",
        "og_desc": "Wood-fired oven at Via Bellinzona 187. Any pizza €5.99, drink +€1, every day 6–11 pm.",
        "og_alt": "The wood-fired oven at Pizzeria Numero 1 in Como",
    },
    "es": {
        "locale": "es_ES",
        "title": "Pizza para llevar y kebab en Como · Numero 1, horno de leña",
        "desc": "Pizzería para llevar y kebab Numero 1, horno de leña en Monte Olimpino, Como. Pizza 5,99 €, bebida +1 €. Abierto todos los días de 18:00 a 23:00.",
        "og_title": "Pizza para llevar y kebab en Como · Numero 1",
        "og_desc": "Horno de leña en Via Bellinzona 187. Pizza a 5,99 €, bebida +1 €, todos los días de 18:00 a 23:00.",
        "og_alt": "El horno de leña de la Pizzeria Numero 1 en Como",
    },
    "de": {
        "locale": "de_DE",
        "title": "Pizza & Kebab zum Mitnehmen in Como · Numero 1, Holzofen",
        "desc": "Pizzeria und Kebab zum Mitnehmen Numero 1, Holzofen in Monte Olimpino, Como. Jede Pizza 5,99 €, Getränk +1 €. Täglich von 18 bis 23 Uhr geöffnet.",
        "og_title": "Pizza & Kebab zum Mitnehmen in Como · Numero 1",
        "og_desc": "Holzofen in der Via Bellinzona 187. Jede Pizza 5,99 €, Getränk +1 €, täglich 18–23 Uhr.",
        "og_alt": "Der Holzofen der Pizzeria Numero 1 in Como",
    },
}


LINKS = {
    "en": {"pizza-a-domicilio-como": "en/pizza-delivery-como", "kebab-como": "en/kebab-como", "domande-frequenti": "en/faq"},
    "es": {"pizza-a-domicilio-como": "es/pizza-a-domicilio-como", "kebab-como": "es/kebab-como", "domande-frequenti": "es/preguntas-frecuentes"},
    "de": {"pizza-a-domicilio-como": "de/pizza-lieferung-como", "kebab-como": "de/kebab-como", "domande-frequenti": "de/haeufige-fragen"},
}


def tag_content(src, pattern, value):
    out, n = re.subn(pattern, lambda m: m.group(1) + html.escape(value, quote=True) + m.group(2), src, count=1)
    assert n == 1, pattern
    return out


def absolute(url):
    if re.match(r"^(?:[a-z]+:|/|#)", url):
        return url
    return "/" + url


def build(src, i18n, lang):
    d, meta = i18n[lang], META[lang]
    out = src.replace('<html lang="it">', '<html lang="%s">' % lang, 1)
    out = tag_content(out, r"(<title>)[^<]*(</title>)", meta["title"])
    out = tag_content(out, r'(<meta name="description" content=")[^"]*(")', meta["desc"])
    out = tag_content(out, r'(<meta property="og:title" content=")[^"]*(")', meta["og_title"])
    out = tag_content(out, r'(<meta property="og:description" content=")[^"]*(")', meta["og_desc"])
    out = tag_content(out, r'(<meta property="og:image:alt" content=")[^"]*(")', meta["og_alt"])
    out = tag_content(out, r'(<meta property="og:locale" content=")[^"]*(")', meta["locale"])
    out = tag_content(out, r'(<link rel="canonical" href=")[^"]*(")', BASE + lang + "/")
    out = tag_content(out, r'(<meta property="og:url" content=")[^"]*(")', BASE + lang + "/")

    def text(m):
        key = m.group(2)
        return m.group(1) + html.escape(d[key], quote=False) + "<" if key in d else m.group(0)

    out = re.sub(r'(<[a-z0-9]+\b[^>]*\bdata-i18n="([^"]+)"[^>]*>)[^<]*<', text, out)

    def aria(m):
        key = re.search(r'data-i18n-aria="([^"]+)"', m.group(0)).group(1)
        if key not in d:
            return m.group(0)
        return re.sub(r'aria-label="[^"]*"', 'aria-label="%s"' % html.escape(d[key], quote=True), m.group(0))

    out = re.sub(r'<[a-z0-9]+\b[^>]*\bdata-i18n-aria="[^"]+"[^>]*>', aria, out)

    out = re.sub(r'\b(src|href|poster)="([^"]+)"', lambda m: '%s="%s"' % (m.group(1), absolute(m.group(2))), out)
    out = re.sub(
        r'\bsrcset="([^"]+)"',
        lambda m: 'srcset="%s"' % ", ".join(absolute(p.strip()) for p in m.group(1).split(",")),
        out,
    )
    out = re.sub(r"url\('([^')]+)'\)", lambda m: "url('%s')" % absolute(m.group(1)), out)
    out = out.replace("'icon-' +", "'/icon-' +").replace("register('sw.js')", "register('/sw.js')")
    for italian, local in LINKS[lang].items():
        out = out.replace('href="/%s/"' % italian, 'href="/%s/"' % local)
    return out


def main():
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    stats_path = os.path.join(ROOT, "tools", "analytics.html")
    stats = open(stats_path, encoding="utf-8").read().strip() if os.path.exists(stats_path) else ""
    marked = re.sub(r"<!-- analytics -->.*?<!-- /analytics -->", lambda m: "<!-- analytics -->" + stats + "<!-- /analytics -->", src, flags=re.S)
    if marked != src:
        src = marked
        with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline=chr(10)) as f:
            f.write(src)
    line = next(l for l in src.split("\n") if l.lstrip().startswith("var I18N = "))
    i18n = json.loads(line[line.index("{"):].rstrip().rstrip(";"))
    for lang in META:
        os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
        with open(os.path.join(ROOT, lang, "index.html"), "w", encoding="utf-8", newline="\n") as f:
            f.write(build(src, i18n, lang))
        print("ok", lang)


if __name__ == "__main__":
    main()
