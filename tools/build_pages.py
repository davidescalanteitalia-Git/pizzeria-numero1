"""Genera las paginas de domicilio, kebab y preguntas frecuentes en it/en/es/de.
Los textos estan en pages_content.py. Ejecutar:  python tools/build_pages.py"""
import html, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages_content import FAQ, PAGES, UI  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://pizzeriakebabnumero1.it/"
LANGS = ["it", "en", "es", "de"]
LOCALE = {"it": "it_IT", "en": "en_GB", "es": "es_ES", "de": "de_DE"}
MAPS = "https://maps.app.goo.gl/hqWGvpCXQUtksS8U6"
WA = "https://wa.me/393334430164"
HOME = {"it": "/", "en": "/en/", "es": "/es/", "de": "/de/"}
SLUG = {
    "dom": {"it": "pizza-a-domicilio-como", "en": "en/pizza-delivery-como", "es": "es/pizza-a-domicilio-como", "de": "de/pizza-lieferung-como"},
    "kebab": {"it": "kebab-como", "en": "en/kebab-como", "es": "es/kebab-como", "de": "de/kebab-como"},
    "faq": {"it": "domande-frequenti", "en": "en/faq", "es": "es/preguntas-frecuentes", "de": "de/haeufige-fragen"},
}


def analytics():
    path = os.path.join(ROOT, "tools", "analytics.html")
    return open(path, encoding="utf-8").read().strip() if os.path.exists(path) else ""


def e(s):
    return html.escape(s, quote=True)


def render_blocks(blocks, lang, links):
    out = []
    for kind, val in blocks:
        if kind == "lede":
            out.append('  <p class="lede">%s</p>' % e(val))
        elif kind == "h2":
            out.append("\n  <h2>%s</h2>" % e(val))
        elif kind == "p":
            out.append("  <p>%s</p>" % val.format(**links))
        elif kind == "note":
            out.append('  <p class="note">%s</p>' % e(val))
        elif kind == "prices":
            rows = "\n".join("    <li><span>%s</span><b>%s</b></li>" % (e(a), e(b)) for a, b in val)
            out.append('  <ul class="plain">\n%s\n  </ul>' % rows)
        elif kind == "items":
            rows = "\n".join(
                "    <li><div><b>%s</b><br><span>%s</span></div>%s</li>" % (e(n), e(d), "<b>%s</b>" % e(p) if p else "")
                for n, d, p in val
            )
            out.append('  <ul class="plain">\n%s\n  </ul>' % rows)
        elif kind == "ul":
            rows = "\n".join("    <li>%s</li>" % v.format(**links) for v in val)
            out.append('  <ul class="dots">\n%s\n  </ul>' % rows)
        elif kind == "faq":
            out.append("")
            for i, (q, a) in enumerate(FAQ[lang]):
                out.append("  <details%s><summary>%s</summary><p>%s</p></details>" % (" open" if i == 0 else "", e(q), e(a)))
    return "\n".join(out)


def build(key, lang):
    page, ui, slug = PAGES[key][lang], UI[lang], SLUG[key][lang]
    url = BASE + slug + "/"
    links = {"menu": HOME[lang] + "#menu", "wa": WA, "maps": MAPS,
             "dom": "/" + SLUG["dom"][lang] + "/", "kebab": "/" + SLUG["kebab"][lang] + "/"}
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Pizzeria Numero 1", "item": BASE + HOME[lang].lstrip("/")},
        {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": url}]}]
    if key == "faq":
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[lang]]})
    alternates = "\n".join('<link rel="alternate" hreflang="%s" href="%s%s/">' % (l, BASE, SLUG[key][l]) for l in LANGS)
    alternates += '\n<link rel="alternate" hreflang="x-default" href="%s%s/">' % (BASE, SLUG[key]["it"])
    stats = analytics()
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(page["title"])}</title>
<meta name="description" content="{e(page["desc"])}">
<link rel="canonical" href="{url}">
{alternates}
<meta name="theme-color" content="#b03a24">
<meta property="og:type" content="website">
<meta property="og:locale" content="{LOCALE[lang]}">
<meta property="og:site_name" content="Pizzeria Numero 1">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(page["title"])}">
<meta property="og:description" content="{e(page["desc"])}">
<meta property="og:image" content="{BASE}forno-a-legna-pizzeria-como.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/pagine.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
{stats}
</head>
<body>

<div class="top"><div class="wrap">
  <a href="{HOME[lang]}" aria-label="{e(ui["home_aria"])}"><img src="/logo-header.png" alt="Pizzeria Kebab Numero 1" width="170" height="197"></a>
  <a class="btn" href="{links["menu"]}" data-ev="ordina">{e(ui["order"])}</a>
</div></div>

<main class="wrap">
  <p class="crumbs"><a href="{HOME[lang]}">Pizzeria Numero 1</a> › {e(page["crumb"])}</p>
  <h1>{e(page["h1"])}</h1>
{render_blocks(page["blocks"], lang, links)}

  <div class="cta">
    <h2>{e(ui["cta_h"])}</h2>
    <p>{e(ui["cta_p"])}</p>
    <a class="btn" href="{links["menu"]}" data-ev="ordina">{e(ui["order_site"])}</a>
    <a class="btn line" href="tel:+390312073720" data-ev="chiama">{e(ui["call"])} 031&nbsp;2073720</a>
    <a class="btn line" href="{WA}" rel="noopener" data-ev="whatsapp">WhatsApp</a>
  </div>
</main>

<footer class="wrap">
  <nav aria-label="{e(ui["nav_aria"])}">
    <a href="{HOME[lang]}">{e(ui["menu"])}</a>
    <a href="{links["dom"]}">{e(ui["dom"])}</a>
    <a href="{links["kebab"]}">{e(ui["kebab"])}</a>
    <a href="/{SLUG["faq"][lang]}/">{e(ui["faq"])}</a>
    <a href="/privacy.html">{e(ui["privacy"])}</a>
  </nav>
  <p>Pizzeria Numero 1 — Pizzeria Noi Tre di Zoheir Abir Sayed Ali A., Via Bellinzona 187, 22100 Como (CO), P.IVA 04221150131</p>
</footer>

</body>
</html>
'''


def main():
    for key in PAGES:
        for lang in LANGS:
            folder = os.path.join(ROOT, *SLUG[key][lang].split("/"))
            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, "index.html"), "w", encoding="utf-8", newline="\n") as f:
                f.write(build(key, lang))
            print("ok", SLUG[key][lang])


if __name__ == "__main__":
    main()
