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
- Location: the Google Business Profile pin (43.7366984, 15.8918039) is
  embedded on the contact page and linked from the footer.

## Needed from the community

**Identity and contact**
- [ ] Full legal name of the community (for the donation page and schema)
- [ ] Street address of the hall - the map pin is in, but the written address
      is still a placeholder in the footer, the contact page and the schema
- [ ] Phone number
- [ ] Confirm `info@krscanskazajednicasibenik.hr` is the right inbox
- [ ] One-line description of the community (used in the footer and meta tags)

**Homepage**
- [ ] Intro paragraph under the main heading
- [ ] Bible verse for the quote block
- [ ] Photograph of the community
- [ ] Any meeting day besides Saturday, if there is one

**Novosti**
- [ ] First few notices: title, date, short text, image
- [ ] Decide: notices edited by hand in `src/pages/novosti/`, or a small admin
      screen later

**O nama**
- [ ] Povijest: key years with what happened, old photographs if any
- [ ] Vodstvo: names, roles, short bios, portrait photos
- [ ] Vjerovanje: the statements of faith with Bible references
- [ ] Decide whether svjedočanstva becomes a fourth item in the dropdown

**Video poruke**
- [ ] Which videos from the YouTube channel go on the page, with title and date

**Knjižnica**
- [ ] Book list: title, author, short description, cover image
- [ ] Later, separately: internal stock screen for the librarian - copies held,
      copies free, who borrowed what. Not public.

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
