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
- **Replacing an image in place does not reach anyone who already has it.**
  Asset file names are stable, so a swapped photo needs a new URL: bump the
  `?v=` on the hero urls in `styles.css`. `vercel.json` serves `/assets/` with
  `must-revalidate` rather than `immutable` for the same reason - `immutable`
  tells a browser never to ask again, which is only safe when the file name
  changes with the content.
- Photographs get exported to WebP at two widths and **saved without EXIF** -
  phone pictures carry GPS coordinates. Check contrast after changing any
  image that sits behind text; the home hero currently clears AAA at 7.2:1.
- The header is **fixed**, not sticky, so it takes no space and every hero
  starts at the very top of the page with its photograph running behind the
  bar. That is why `.hero` adds `--header-h` to its own top padding - a new
  page without a hero would slide under the header.
- Person grids use `auto-fill`, never `auto-fit`. `auto-fit` collapses the
  empty tracks, so a section with two people would stretch their portraits to
  twice the size of a section with four.
- `build.py` reads with `utf-8-sig`. A BOM at the start of a partial is not
  whitespace and renders as a real line box, which once pushed the whole page
  down by a line. PowerShell's `-Encoding UTF8` writes one - prefer the Write
  tool, or `System.Text.UTF8Encoding($false)`.
- The header is transparent while it is over the hero and solid after it.
- **The home hero is dark and its copy is light**; every other page is the
  light paper scheme. The dark overlay is what makes the white copy and white
  menu legible, so it is not a style choice to soften casually - measured at
  5.2:1 for the copy and 7.9:1 for the menu. Re-measure if the photograph
  changes. Everything light-on-dark is scoped to
  `.page-home .site-header:not(.is-stuck)`, so the bar reverts to dark-on-light
  the moment it goes solid.
- `.site-header::before` is a light scrim for the inner pages, switched off on
  the home page where it would only fight the dark hero.
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
