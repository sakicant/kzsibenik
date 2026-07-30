# kzsibenik

Website for **Kršćanska zajednica Šibenik** - krscanskazajednicasibenik.hr

Static site, no framework, no build dependencies beyond Python. Croatian at the
site root, English under `/en/`.

## Build

```bash
python build.py
```

That reads `src/` and writes the `index.html` files plus `sitemap.xml` into the
project root. Run it after editing any page or partial. Never hand-edit a
generated `index.html` - the next build overwrites it.

## Preview locally

```bash
python -m http.server 5510
```

Then open http://localhost:5510/

## Structure

```
build.py                 build script
styles.css               all styling, tokens at the top
script.js                header, mobile menu, dropdown, reveals
contact.php              contact form mailer (FTP hosting only)
vercel.json              preview hosting config
src/partials/            base.html, header.<lang>.html, footer.<lang>.html
src/pages/<id>/<lang>/   meta.json + content.html per page and language
assets/img/              logo, mark, OG image
```

Everything outside `src/` at the root that looks like a page folder
(`o-nama/`, `en/`, ...) is generated output.

## Pages

| page-id | Croatian | English |
|---|---|---|
| home | `/` | `/en/` |
| novosti | `/novosti/` | `/en/news/` |
| o-nama | `/o-nama/` | `/en/about/` |
| povijest | `/o-nama/povijest/` | `/en/about/history/` |
| vodstvo | `/o-nama/vodstvo/` | `/en/about/leadership/` |
| vjerovanje | `/o-nama/vjerovanje/` | `/en/about/beliefs/` |
| video-poruke | `/video-poruke/` | `/en/messages/` |
| knjiznica | `/knjiznica/` | `/en/library/` |
| doniraj | `/doniraj/` | `/en/give/` |
| kontakt | `/kontakt/` | `/en/contact/` |

Menu shape: Naslovna, Novosti, O nama, Multimedija, Doniraj, Kontakt.

"O nama" is both a page and a dropdown - the label links to `/o-nama/` and the
small caret beside it opens Povijest, Vodstvo, Vjerovanje. "Multimedija" is a
dropdown label only, with Video poruke and Knjižnica under it; those two keep
their own top-level slugs.

## Adding a page

1. Create `src/pages/<page-id>/hr/` with `meta.json` and `content.html`.
2. Do the same under `en/`.
3. Add the link to `src/partials/header.hr.html` and `header.en.html` (and the
   footers).
4. Run `python build.py`.

`meta.json` fields: `slug` (no leading or trailing slash), `title`,
`description`, optional `parents` for the breadcrumb, optional `schema`,
optional `body_class`.

## Hosting

Currently on Vercel for preview and review. Moving to FTP hosting later.

The contact form posts to `/contact.php`, which only runs on the FTP host.
On the Vercel preview the form renders but submitting does nothing.

When moving to FTP: upload everything except `src/`, `build.py`, `.git/` and
`vercel.json`. **Upload in binary mode** - ASCII mode corrupts PHP files.

## Still to do

See [TODO-content.md](TODO-content.md).
