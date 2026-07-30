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

## Open items

See `TODO-content.md`.
