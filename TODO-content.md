# Content still to supply

The site is built as structure only - layout, navigation and headings are real,
body copy is not written yet. Every gap is visible on the page as a grey
skeleton bar, a dotted-underline italic string, or a note in a gold box.

To find them all in the source:

```bash
grep -rn "data-placeholder\|ph-lines\|ph-note\|ph-media" src/pages/
```

## Already known

- Meetings: **every Saturday at 19:00**. Wired into the homepage schedule, the
  contact page, the footer and the schema on the homepage.
- YouTube: **@krscanskazajednicasibenik**. Linked from the video messages page,
  the homepage, the footer and `sameAs` in the schema.
- Location: **Ul. Šibenske narodne glazbe 3, 22000 Šibenik**. In the footer,
  the contact page and the schema. The Google Business Profile pin
  (43.7366984, 15.8918039) is embedded on the contact page.
- Eldership: Marijan Kuvačić, Ivica Šupe, Frane Cinotti, Ante Mikulandra.

## Needed from the community

**Identity and contact**
- [ ] Full legal name of the community (for the donation page and schema)
- [ ] Phone number
- [ ] Confirm `info@krscanskazajednicasibenik.hr` is the right inbox
- [ ] Facebook and Instagram page URLs. Both show as greyed, unclickable icons
      in the footer until they arrive; the comment above the block in
      `src/partials/footer.*.html` says exactly what to swap.
- [ ] One-line description of the community (used in the footer and meta tags)

**Homepage**
- [ ] Intro paragraph under the main heading
- [ ] Bible verse for the quote block
- [ ] Any meeting day besides Saturday, if there is one
- [ ] **Hero photograph is a temporary stand-in** (Šibenik centre park). To
      swap it, drop the replacement over `assets/img/hero-sibenik.webp` and
      `hero-sibenik-mobile.webp` at 1600px and 1000px wide. If the new picture
      is much darker, re-check the overlay in `styles.css` - the text sits on
      the left and currently clears AAA at 7.2:1.
- Done: community photograph in the "O nama" block. EXIF, GPS included, is
      stripped from the exported WebP.

**Novosti**
- [ ] First few notices: title, date, short text, image
- Decided: notices and YouTube videos get managed through an admin panel at
      `/isusjekralj/`. Spec in [plans/admin-panel.md](plans/admin-panel.md).
      Needs PHP and MySQL on the FTP host, so it cannot be built against the
      Vercel preview.

**O nama**
- [ ] Povijest: key years with what happened, old photographs if any
- [ ] Vodstvo: portrait photos and short bios for the four elders; the whole
      worship team and technical team sections are still placeholders
- [ ] Vjerovanje: the statements of faith with Bible references
- [ ] Decide whether svjedočanstva becomes a fourth item in the dropdown

**Video poruke**
- [ ] Which videos from the YouTube channel go on the page, with title and date

**Knjižnica**
- [ ] Book list for the public page: title, author, short description, cover
      image. Static, edited in `src/pages/knjiznica/`.
- Decided: the librarian gets her own inventory screens inside the admin panel
      (stock, availability, who borrowed what), with no link to the public
      page. See `plans/admin-panel.md`.

**Doniraj**
- [ ] Recipient name, IBAN, model and reference number, payment description
- [ ] Optional: a note on what the giving supports
- [ ] Decide whether online card payment is wanted

## Design decisions still open

- [ ] Brand colours. Everything currently runs on neutral grey plus one muted
      brass accent. All of it lives in the `:root` block at the top of
      `styles.css` - changing those values re-skins the whole site.
- [ ] Final logo. The current pack is the working version; the header uses the
      black logo on light, the footer the white logo on dark.
- [ ] English translations of the real Croatian copy, once it exists.

## Technical

- [ ] Point krscanskazajednicasibenik.hr at the host once ready
- [ ] Move from Vercel to FTP hosting (upload in binary mode)
- [ ] Test the contact form on the FTP host - it cannot work on Vercel
- [ ] `favicon.ico` is not in the logo pack; only PNG icons are wired up. Fine
      for modern browsers, add an `.ico` if old ones matter.
