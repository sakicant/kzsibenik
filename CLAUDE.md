# kzsibenik - working notes

Website for Kršćanska zajednica Šibenik (krscanskazajednicasibenik.hr).

## Rules

- **Never hand-edit a generated `index.html`.** Edit `src/pages/…` or
  `src/partials/…`, then run `python build.py`.
- Croatian is the primary language at the site root. English lives under
  `/en/`. Every page must exist in both, or the language switcher falls back
  to that language's home page.
- Croatian slugs are Croatian words (`o-nama/povijest`), English slugs are
  English words (`about/history`). They are paired by page-id, not by slug.
- Header order is fixed: Naslovna, Novosti, O nama, Multimedija, Doniraj,
  Kontakt. No item is styled as a call-to-action button.
- "O nama" is a link **and** a dropdown: the label goes to `/o-nama/`, the
  caret button beside it opens the three children. "Multimedija" is a plain
  dropdown button with no page behind it.
- Every `main > section` past the hero gets a Š watermark from
  `styles.css`, cycling left, right, centre. It is automatic - do not add
  watermark markup to pages.
- The language switcher markup, flags included, is generated in `build.py`
  (`build_lang_switcher`). Do not hand-write it into a partial. Flags are
  inline SVG on purpose: Windows renders emoji flags as bare letter pairs.
- The hero countdown targets Saturday 19:00 **Europe/Zagreb**, not the
  visitor's zone, and handles both DST switches. Its strings come from
  `data-` attributes on `.hero-meta` so `script.js` stays language-agnostic.
  The static sentence inside is the no-JS fallback - keep it meaningful.
- Photographs get exported to WebP at two widths and **saved without EXIF** -
  phone pictures carry GPS coordinates. Check contrast after changing any
  image that sits behind text; the home hero currently clears AAA at 7.2:1.
- All colour lives in the `:root` block at the top of `styles.css`. The brand
  colours are not decided yet, so do not hardcode a hex value anywhere else.
- Body copy is not written yet. Placeholders are deliberate and visible:
  `.ph-lines` skeleton bars, `[data-placeholder]` inline strings, `.ph-note`
  boxes, `.ph-media` image slots. Do not invent church copy to fill them.
- Check mobile, not just desktop. Breakpoints are 1040 / 900 / 860 / 620 / 400.

## Build

`python build.py` reads `src/`, writes page folders and `sitemap.xml`, and
stamps `styles.css` / `script.js` with a content hash for cache busting.

## Hosting

Vercel now (preview and review), FTP later. `contact.php` only runs on the FTP
host - the form is inert on Vercel. When uploading over FTP use **binary
mode**; ASCII mode corrupts PHP and produces 500s.

## Admin panel

Planned, not built. Spec in `plans/admin-panel.md`. It needs PHP and MySQL, so
it can only run on the FTP host, never on the Vercel preview.

## Open items

See `TODO-content.md`.
