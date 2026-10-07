#!/usr/bin/env python3
"""Ģenerē /en/, /de/, /ru/ no index.html (LV avots).

Rediģē tikai index.html (LV teksts + I18N vārdnīca skriptā) un META zemāk,
tad palaid:  python3 build.py
Katrai valodai ir savs URL, <html lang>, title/meta, canonical, hreflang un FAQ JSON-LD.
Teksts no I18N tiek ierakstīts statiski (meklētājiem); skripts to pašu pielieto arī pārlūkā.
"""
import json, os, re, subprocess

SRC = "index.html"
BASE = "https://lipinasenergy.com"
URL = {"lv": "/", "en": "/en/", "de": "/de/", "ru": "/ru/"}
LOCALE = {"lv": "lv_LV", "en": "en_US", "de": "de_DE", "ru": "ru_RU"}

META = {
    "en": {
        "org": "“STROIPERLIT-RIGA” Ltd (SIA)",
        "capex": "~€2.3M",
        "title": "Ļipiņas SES + BESS Park — Solar and Battery Storage Project",
        "desc": "Ļipiņas SES + BESS: 3 MW solar system with 5 MWh battery storage in Salaspils region, next to Knauf. Investment opportunity in Baltic renewables.",
        "og_desc": "3 MW solar system with 5 MWh battery storage in Salaspils region. Investment opportunity in the Baltic renewable energy sector.",
        "tw_title": "Ļipiņas SES + BESS Park",
        "tw_desc": "3 MW solar system + 5 MWh battery storage in Salaspils region. Investment opportunity.",
        "site_desc": "3 MW solar energy system with 5 MWh battery energy storage in Salaspils region, Latvia.",
        "place_desc": "3 MW solar energy system (SES) and 5 MWh battery energy storage system (BESS) on the plots \"Ļipiņas\" and \"Ļipiņas 1\".",
    },
    "de": {
        "org": "„STROIPERLIT-RIGA“ GmbH (SIA)",
        "capex": "~€2,3M",
        "title": "Ļipiņas SES + BESS Park — Solar- und Batteriespeicherprojekt",
        "desc": "Ļipiņas SES + BESS: 3-MW-Solaranlage mit 5 MWh Batteriespeicher in Salaspils, neben Knauf. Investitionsmöglichkeit im baltischen Energiesektor.",
        "og_desc": "3-MW-Solaranlage mit 5 MWh Batteriespeicher in der Gemeinde Salaspils. Investitionsmöglichkeit im baltischen Sektor für erneuerbare Energien.",
        "tw_title": "Ļipiņas SES + BESS Park",
        "tw_desc": "3-MW-Solaranlage + 5 MWh Batteriespeicher in der Gemeinde Salaspils. Investitionsmöglichkeit.",
        "site_desc": "3-MW-Solarenergiesystem mit 5 MWh Batterie-Energiespeicher in der Gemeinde Salaspils, Lettland.",
        "place_desc": "3-MW-Solarenergiesystem (SES) und 5-MWh-Batterie-Energiespeichersystem (BESS) auf den Grundstücken „Ļipiņas“ und „Ļipiņas 1“.",
    },
    "ru": {
        "org": "ООО «STROIPERLIT-RIGA» (SIA)",
        "capex": "~€2,3M",
        "title": "Ļipiņas СЭС + BESS — солнечная энергия и накопители",
        "desc": "Ļipiņas СЭС + BESS: солнечная система 3 МВт с накопителем 5 МВт·ч в Саласпилсском крае, рядом с Knauf. Инвестиции в возобновляемую энергетику Балтии.",
        "og_desc": "Солнечная система 3 МВт с накопителем 5 МВт·ч в Саласпилсском крае. Инвестиционная возможность в секторе возобновляемой энергии Балтии.",
        "tw_title": "Парк Ļipiņas СЭС + BESS",
        "tw_desc": "Солнечная система 3 МВт + накопитель 5 МВт·ч в Саласпилсском крае. Инвестиционная возможность.",
        "site_desc": "Солнечная энергосистема 3 МВт с накопителем энергии 5 МВт·ч в Саласпилсском крае, Латвия.",
        "place_desc": "Солнечная энергосистема (СЭС) 3 МВт и система накопления энергии (BESS) 5 МВт·ч на участках «Ļipiņas» и «Ļipiņas 1».",
    },
}


# Statiskās skaitļu vērtības pēc valodas (LV avots → valoda); decimālzīme, tūkstošu atdalītājs, mērvienības
N = "\u00a0"
SPEC = {
    "en": [("3"+N+"MWp", "3"+N+"MWp"), ("5"+N+"MWh", "5"+N+"MWh"), ("2,5"+N+"MW", "2.5"+N+"MW"),
           ("4,5"+N+"MWh", "4.5"+N+"MWh"), ("4,2"+N+"ha", "4.2"+N+"ha"), ("4"+N+"304", "4,304"),
           ("3"+N+"077"+N+"kW", "3,077"+N+"kW"), ("2384 × 1303"+N+"mm", "2384 × 1303"+N+"mm")],
    "de": [],
    "ru": [("3"+N+"MWp", "3"+N+"МВт (пик)"), ("5"+N+"MWh", "5"+N+"МВт·ч"), ("2,5"+N+"MW", "2,5"+N+"МВт"),
           ("4,5"+N+"MWh", "4,5"+N+"МВт·ч"), ("4,2"+N+"ha", "4,2"+N+"га"), ("4"+N+"304", "4"+N+"304"),
           ("3"+N+"077"+N+"kW", "3"+N+"077"+N+"кВт"), ("2384 × 1303"+N+"mm", "2384 × 1303"+N+"мм")],
}


def load_i18n(src):
    js = re.search(r"const I18N = (\{.*?\n\});", src, re.S).group(1)
    out = subprocess.run(
        ["node", "-e", "const I=" + js + ";process.stdout.write(JSON.stringify(I))"],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def esc_attr(t):
    return t.replace("&", "&amp;").replace('"', "&quot;")


def set_text(html, attr, d):
    # <tag ... data-i18n="k" ...>…</tag>; elementi nav ligzdoti vienādā tagā
    pat = re.compile(r'(<(\w+)\b[^>]*\b%s="([^"]+)"[^>]*>)(.*?)(</\2>)' % attr, re.S)

    def f(m):
        k = m.group(3)
        if k not in d:
            return m.group(0)
        return m.group(1) + d[k] + m.group(5)
    return pat.sub(f, html)


def meta(html, name, val, attr="name"):
    pat = re.compile(r'(<meta %s="%s" content=")[^"]*(">)' % (attr, re.escape(name)))
    html, n = pat.subn(lambda m: m.group(1) + esc_attr(val) + m.group(2), html)
    assert n == 1, name
    return html


def build(lang, src, I18N):
    d, M = I18N[lang], META[lang]
    h = src
    h = h.replace('<html lang="lv">', '<html lang="%s">' % lang, 1)
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % M["title"], h, 1)
    h = meta(h, "description", M["desc"])
    h = meta(h, "og:title", M["title"], "property")
    h = meta(h, "og:description", M["og_desc"], "property")
    h = meta(h, "og:url", BASE + URL[lang], "property")
    h = meta(h, "og:locale", LOCALE[lang], "property")
    h = re.sub(r'(<meta property="og:locale:alternate" content="[^"]*">\n)+',
               "".join('<meta property="og:locale:alternate" content="%s">\n' % LOCALE[l] for l in URL if l != lang), h, 1)
    h = meta(h, "twitter:title", M["tw_title"])
    h = meta(h, "twitter:description", M["tw_desc"])
    # uzņēmuma nosaukums pēc valodas (legalName paliek reģistrētais LV nosaukums)
    lv_org = "SIA „STROIPERLIT-RIGA“"
    h = meta(h, "author", M["org"])
    for old, new in SPEC[lang]:
        old_b, new_b = "<b>%s</b>" % old, "<b>%s</b>" % new
        assert h.count(old_b) == 1, old_b
        h = h.replace(old_b, new_b)
    old = '<div class="n">~€2,3M</div><div class="l" data-i18n="fin_capex">'
    assert h.count(old) == 1, old
    h = h.replace(old, old.replace("~€2,3M", M["capex"]))
    for old, new in (('"name": "%s",' % lv_org, '"name": "%s",' % M["org"]),
                     ("<h3>%s</h3>" % lv_org, "<h3>%s</h3>" % M["org"])):
        assert h.count(old) == 1, old
        h = h.replace(old, new)
    h = h.replace('<link rel="canonical" href="%s/">' % BASE, '<link rel="canonical" href="%s%s">' % (BASE, URL[lang]), 1)
    h = h.replace('"inLanguage": ["lv", "en", "de", "ru"],', '"inLanguage": ["lv", "en", "de", "ru"],', 1)
    # JSON-LD apraksti
    lv_site = re.search(r'"description": "(3 MW saules enerģijas sistēma ar 5 MWh akumulatoru enerģijas uzkrāšanas sistēmu Salaspils novadā, Latvijā\.)"', h).group(1)
    h = h.replace(lv_site, M["site_desc"], 1)
    lv_place = re.search(r'"description": "(3 MW saules enerģijas sistēma \(SES\) un 5 MWh[^\n]*?)",\n', h).group(1)
    h = h.replace(lv_place, M["place_desc"].replace('"', '\\"'), 1)
    # FAQ JSON-LD
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": d["faq_q%d" % i],
         "acceptedAnswer": {"@type": "Answer", "text": d["faq_a%d" % i]}} for i in range(1, 6)]}
    h = re.sub(r'(<script type="application/ld\+json">\n)\{\n  "@context": "https://schema.org",\n  "@type": "FAQPage".*?\n\}(\n</script>)',
               lambda m: m.group(1) + json.dumps(faq, ensure_ascii=False, indent=2) + m.group(2), h, 1, flags=re.S)
    # saturs
    h = set_text(h, "data-i18n-html", d)
    h = set_text(h, "data-i18n", d)
    # valodu pārslēgs
    h = re.sub(r'(<a href="[^"]*" hreflang="\w+" data-lang="\w+") class="on"', r"\1", h)
    h = re.sub(r'(<a href="[^"]*" hreflang="%s" data-lang="%s")' % (lang, lang), r'\1 class="on"', h, 1)
    return h


def main():
    src = open(SRC, encoding="utf-8").read()
    I18N = load_i18n(src)
    for lang in ("en", "de", "ru"):
        os.makedirs(lang, exist_ok=True)
        with open(os.path.join(lang, "index.html"), "w", encoding="utf-8") as f:
            f.write(build(lang, src, I18N))
        print("OK", lang)


if __name__ == "__main__":
    main()
