"""Static site build script for krscanskazajednicasibenik.hr.

Each page lives in src/pages/<page-id>/<lang>/ as a meta.json + content.html
pair. <page-id> groups the translations of one logical page together (e.g.
"povijest"); <lang> is an ISO 639-1 code. Croatian is canonical and served at
the site root (e.g. /o-nama/); English is served under /en/ (e.g. /en/about/).

For every page-id the script generates reciprocal hreflang alternates across
all language variants that exist, plus an x-default pointing at Croatian.

Run `python build.py` after editing any partial or page content.
"""
import datetime
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
PAGES_DIR = os.path.join(SRC, "pages")
PARTIALS_DIR = os.path.join(SRC, "partials")

SITE_URL = "https://krscanskazajednicasibenik.hr"
DEFAULT_OG_IMAGE = f"{SITE_URL}/assets/img/og-image.png"

# Croatian is the primary language, served at the site root.
DEFAULT_LANG = "hr"

# Supported languages. Codes must be valid ISO 639-1 for correct hreflang.
LANGUAGES = ["hr", "en"]

HOME_LABEL = {"hr": "Naslovna", "en": "Home"}
LANGUAGE_LABELS = {"hr": "HR", "en": "EN"}

# Pages that sit high in the sitemap. Keys are page-ids, not slugs, so the
# priority holds across both languages.
PRIORITY_BY_PAGE = {
    "home": "1.0",
    "novosti": "0.9",
    "o-nama": "0.9",
    "video-poruke": "0.8",
    "kontakt": "0.8",
    "doniraj": "0.7",
    "knjiznica": "0.6",
}


def compute_asset_version():
    """Short hash of styles.css + script.js so browsers fetch fresh copies
    whenever either file changes instead of serving a stale cached copy."""
    hasher = hashlib.md5()
    for name in ("styles.css", "script.js"):
        with open(os.path.join(ROOT, name), "rb") as f:
            hasher.update(f.read())
    return hasher.hexdigest()[:10]


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def url_path(lang, slug):
    """Root-relative path (no domain), e.g. / or /en/about/history/."""
    if lang == DEFAULT_LANG:
        path = f"{slug}/" if slug else ""
    else:
        path = f"{lang}/{slug}/" if slug else f"{lang}/"
    return f"/{path}"


def canonical_url(lang, slug):
    return f"{SITE_URL}{url_path(lang, slug)}"


def output_path(lang, slug):
    """Slugs may be nested ("o-nama/povijest"); split on / so the same source
    works on Windows and Linux."""
    parts = [p for p in slug.split("/") if p]
    if lang != DEFAULT_LANG:
        parts.insert(0, lang)
    return os.path.join(ROOT, *parts, "index.html")


def discover_pages():
    """Returns {page_id: {lang: meta_dict}} for every page-id/lang combo found."""
    pages = {}
    for page_id in sorted(os.listdir(PAGES_DIR)):
        page_dir = os.path.join(PAGES_DIR, page_id)
        if not os.path.isdir(page_dir):
            continue
        variants = {}
        for lang in sorted(os.listdir(page_dir)):
            lang_dir = os.path.join(page_dir, lang)
            meta_path = os.path.join(lang_dir, "meta.json")
            if lang not in LANGUAGES or not os.path.isfile(meta_path):
                continue
            with open(meta_path, "r", encoding="utf-8") as f:
                variants[lang] = json.load(f)
        if variants:
            pages[page_id] = variants
    return pages


def build_hreflang_block(variants):
    links = []
    for lang in LANGUAGES:
        if lang not in variants:
            continue
        url = canonical_url(lang, variants[lang].get("slug", ""))
        links.append(f'<link rel="alternate" hreflang="{lang}" href="{url}">')
    if DEFAULT_LANG in variants:
        default_url = canonical_url(DEFAULT_LANG, variants[DEFAULT_LANG].get("slug", ""))
        links.append(f'<link rel="alternate" hreflang="x-default" href="{default_url}">')
    return "\n".join(links)


# Inline flags rather than emoji: Windows renders emoji flags as bare letter
# pairs, so a 🇭🇷 would show up as "HR" for a large share of visitors.
# No ids or clipPaths inside - the same markup is emitted more than once
# per page and duplicate ids would collide.
FLAG_SVG = {
    "hr": (
        '<svg class="flag" viewBox="0 0 60 30" aria-hidden="true">'
        '<rect width="60" height="10" fill="#ff0000"/>'
        '<rect y="10" width="60" height="10" fill="#fff"/>'
        '<rect y="20" width="60" height="10" fill="#171796"/>'
        '<rect x="24.5" y="7.5" width="11" height="12" fill="#fff" stroke="#171796" stroke-width="1"/>'
        '<path fill="#ff0000" d="M24.5 7.5h2.75v3H24.5zm5.5 0h2.75v3H30zm-2.75 3H30v3h-2.75zm5.5 0h2.75v3h-2.75z'
        'M24.5 13.5h2.75v3H24.5zm5.5 0h2.75v3H30zm-2.75 3H30v3h-2.75zm5.5 0h2.75v3h-2.75z"/>'
        "</svg>"
    ),
    "en": (
        '<svg class="flag" viewBox="0 0 60 30" aria-hidden="true">'
        '<rect width="60" height="30" fill="#012169"/>'
        '<path d="M0 0l60 30M60 0L0 30" stroke="#fff" stroke-width="6"/>'
        '<path d="M0 0l60 30M60 0L0 30" stroke="#c8102e" stroke-width="3"/>'
        '<path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/>'
        '<path d="M30 0v30M0 15h60" stroke="#c8102e" stroke-width="6"/>'
        "</svg>"
    ),
}

LANGUAGE_NAMES = {"hr": "Hrvatski", "en": "English"}
SWITCHER_LABEL = {"hr": "Jezik", "en": "Language"}


def build_lang_switcher(variants, current_lang, context):
    """Flag switcher. A language links to its own translation of the current
    page when one exists; otherwise it falls back to that language's home.

    On desktop it is a dropdown showing the current flag and code. In the
    mobile menu it is a plain row of both flags, since a dropdown inside an
    already-open menu is one tap too many."""
    if len(LANGUAGES) < 2:
        return ""

    def link(lang, extra_class=""):
        target = variants[lang].get("slug", "") if lang in variants else ""
        url = url_path(lang, target)
        current = ' aria-current="true"' if lang == current_lang else ""
        cls = ("lang-item is-active" if lang == current_lang else "lang-item")
        if extra_class:
            cls += " " + extra_class
        return (f'<a href="{url}" class="{cls}" hreflang="{lang}" lang="{lang}"{current}>'
                f'{FLAG_SVG[lang]}<span>{LANGUAGE_LABELS[lang]}</span>'
                f'<span class="sr-only"> - {LANGUAGE_NAMES[lang]}</span></a>')

    aria = SWITCHER_LABEL[current_lang]

    if context == "mobile":
        return (f'<div class="lang-switch lang-switch-row" role="group" aria-label="{aria}">'
                + "".join(link(lang) for lang in LANGUAGES)
                + "</div>")

    menu_id = "langMenu"
    return (
        '<div class="lang-switch nav-drop" data-drop>'
        f'<button type="button" class="nav-drop-btn lang-current" aria-expanded="false" '
        f'aria-controls="{menu_id}" aria-label="{aria}">'
        f'{FLAG_SVG[current_lang]}<span>{LANGUAGE_LABELS[current_lang]}</span>'
        '<span class="caret" aria-hidden="true"></span>'
        "</button>"
        f'<div class="nav-drop-menu lang-menu" id="{menu_id}">'
        + "".join(link(lang) for lang in LANGUAGES)
        + "</div></div>"
    )


_PARTIAL_CACHE = {}


def load_partial(name, lang):
    """Return <name>.<lang>.html if it exists, else the shared <name>.html."""
    key = (name, lang)
    if key not in _PARTIAL_CACHE:
        localized = os.path.join(PARTIALS_DIR, f"{name}.{lang}.html")
        path = localized if os.path.isfile(localized) else os.path.join(PARTIALS_DIR, f"{name}.html")
        _PARTIAL_CACHE[key] = read(path)
    return _PARTIAL_CACHE[key]


def mark_active_nav(header_html, slug, lang):
    """Add aria-current + .is-active to the nav link pointing at this exact
    page, so the current tab is visibly marked. Matching is exact, otherwise
    /o-nama/ would light up every child in the dropdown. Marking the dropdown
    button itself is left to script.js, which looks for aria-current inside."""
    prefix = "" if lang == DEFAULT_LANG else f"/{lang}"
    # The home page has an empty slug, so its nav link is just the prefix root.
    needle = f'href="{prefix}/{slug}/"' if slug else f'href="{prefix}/"'
    out = []
    for line in header_html.split("\n"):
        # The logo also points at the home page; it is not a nav item.
        if needle in line and "lang-item" not in line and 'class="brand"' not in line:
            line = line.replace("<a ", '<a aria-current="page" ', 1)
            if 'class="' in line:
                line = line.replace('class="', 'class="is-active ', 1)
            else:
                line = line.replace("<a ", '<a class="is-active" ', 1)
        out.append(line)
    return "\n".join(out)


def build_variant(lang, meta, content_path, base_tpl, hreflang_block, variants, asset_version):
    body = read(content_path)
    slug = meta.get("slug", "")
    canonical = canonical_url(lang, slug)
    footer_html = load_partial("footer", lang)
    header_html = load_partial("header", lang)
    header_html = header_html.replace("{{LANG_SWITCHER_DESKTOP}}",
                                      build_lang_switcher(variants, lang, "desktop"))
    header_html = header_html.replace("{{LANG_SWITCHER_MOBILE}}",
                                      build_lang_switcher(variants, lang, "mobile"))
    header_html = mark_active_nav(header_html, meta.get("nav_slug", slug), lang)

    schema = meta.get("schema")
    schema_list = schema if isinstance(schema, list) else ([schema] if schema else [])
    if slug:  # Auto breadcrumb (Home > … > this page) on every page except home.
        crumbs = [{"@type": "ListItem", "position": 1, "name": HOME_LABEL[lang],
                   "item": canonical_url(lang, "")}]
        for parent in meta.get("parents", []):
            crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1,
                           "name": parent["name"], "item": f"{SITE_URL}{parent['url']}"})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1,
                       "name": meta["title"].split("|")[0].strip(), "item": canonical})
        schema_list = list(schema_list) + [{
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": crumbs,
        }]
    schema_block = "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(s, indent=2, ensure_ascii=False) + "\n</script>"
        for s in schema_list
    )

    html = base_tpl
    replacements = {
        "{{LANG}}": lang,
        "{{TITLE}}": meta["title"],
        "{{DESCRIPTION}}": meta["description"],
        "{{CANONICAL}}": canonical,
        "{{HREFLANGS}}": hreflang_block,
        "{{OG_IMAGE}}": meta.get("og_image", DEFAULT_OG_IMAGE),
        "{{OG_LOCALE}}": {"hr": "hr_HR", "en": "en_US"}[lang],
        "{{SCHEMA}}": schema_block,
        "{{ASSET_VERSION}}": asset_version,
        "{{BODY_CLASS}}": meta.get("body_class", ""),
        "{{HEADER}}": header_html,
        "{{FOOTER}}": footer_html,
        "{{BODY}}": body,
    }
    for k, v in replacements.items():
        html = html.replace(k, v)

    out_path = output_path(lang, slug)
    write(out_path, html)
    return os.path.relpath(out_path, ROOT)


def write_sitemap(pages):
    today = datetime.date.today().isoformat()
    entries = []
    for page_id, variants in pages.items():
        alts = [(lang, canonical_url(lang, variants[lang].get("slug", "")))
                for lang in LANGUAGES if lang in variants]
        default_lang = DEFAULT_LANG if DEFAULT_LANG in variants else next(iter(variants))
        xdefault = canonical_url(default_lang, variants[default_lang].get("slug", ""))
        priority = PRIORITY_BY_PAGE.get(page_id, "0.7")
        for lang, meta in variants.items():
            entries.append((canonical_url(lang, meta.get("slug", "")), priority, alts, xdefault))
    entries.sort(key=lambda e: e[0])

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
             'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for loc, prio, alts, xdefault in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        for lang, href in alts:
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{xdefault}"/>')
        lines.append("  </url>")
    lines.append("</urlset>")
    write(os.path.join(ROOT, "sitemap.xml"), "\n".join(lines) + "\n")
    return len(entries)


def main():
    asset_version = compute_asset_version()
    base_tpl = read(os.path.join(PARTIALS_DIR, "base.html"))
    pages = discover_pages()
    built = 0
    for page_id, variants in pages.items():
        hreflang_block = build_hreflang_block(variants)
        for lang, meta in variants.items():
            content_path = os.path.join(PAGES_DIR, page_id, lang, "content.html")
            rel = build_variant(lang, meta, content_path, base_tpl,
                                hreflang_block, variants, asset_version)
            print(f"built {rel}")
            built += 1
    count = write_sitemap(pages)
    print(f"built sitemap.xml ({count} URLs)")
    print(f"\n{built} pages, asset version {asset_version}")


if __name__ == "__main__":
    main()
