# Admin panel - spec

**Status: planned, not built.** Written down from the brief so the next session
starts from an agreed shape rather than guessing.

## What it is

A private admin screen at `/isusjekralj/`, unlisted. Nothing on the public site
links to it; you reach it by typing the URL. Several people log in with their
own account, and what each one can touch depends on their role.

Through it the community adds **news notices** and **YouTube videos**.
Everything else on the site, the library included, stays static and is edited
in `src/` and rebuilt with `build.py`.

## Before any of it can be built

**Confirmed: the FTP host will have MySQL and PHP.** The Vercel preview is
static, so the panel cannot exist there at all - it only works once the site
sits on the FTP host. Still needed to start:

- [ ] Database name, user and password
- [ ] PHP version on the host

## The library is a separate thing

Settled: the library service gets its own small backend inside the panel,
holding the catalogue, the stock and the borrowing state. **It is not connected
to the front end in any way** - the public `/knjiznica/` page stays static and
is edited in `src/pages/knjiznica/`.

So a `library` user logs into the same panel and sees only their own inventory
screens. Nothing they do there changes a public page.

## Roles

| Role | Can do |
|---|---|
| `superadmin` | Everything, including creating and disabling other accounts |
| `news` | Add, edit and unpublish news notices |
| `video` | Add, edit and remove YouTube videos |
| `library` | The library inventory only. Nothing public. |

Permissions are checked on every request on the server, not just hidden in the
menu. A `news` user who types the video URL directly gets refused.

## Data

**users** - id, name, email, password_hash, role, active, created_at,
last_login_at

**news** - id, slug, lang, title, body, excerpt, image, tag, published_at,
status (draft/published), author_id, created_at, updated_at

**videos** - id, youtube_id, title, description, published_at, duration,
sort_order, status, author_id

News is bilingual, so either one row per language linked by a shared key, or
HR and EN columns on one row. One row per language matches how `src/pages`
already works.

**books** - id, title, author, isbn, category, copies_total, notes

**loans** - id, book_id, borrower_name, borrowed_at, due_at, returned_at

Copies available is derived: `copies_total` minus the loans with no
`returned_at`. Storing it as its own column would drift out of sync.

## Security rules

- Passwords stored with `password_hash()` / `password_verify()`, never plain
  text and never in git. **Antonio creates the first account's password
  himself** - it does not get written into a file here.
- Sessions with `httponly`, `secure` and `samesite=Lax` cookies
- CSRF token on every form that writes
- Login rate limiting: lock out after a handful of failed attempts
- All admin pages send `X-Robots-Tag: noindex, nofollow`
- **`/isusjekralj/` deliberately stays out of `robots.txt`.** Listing it there
  would publish the path to anyone who reads the file. Unlisted plus noindex is
  the right combination; robots.txt would defeat the point.
- Uploaded images: validate the real mime type, cap the size, rename on save,
  store outside any directory that can execute PHP
- `config.php` holds the DB credentials and is already gitignored

Being unlisted is not by itself security. Real accounts with real passwords are
what protect it; the obscure path just keeps it out of sight.

## Videos are typed in by hand

**Decided: no YouTube API.** Whoever adds a video pastes the link and types the
title and date themselves. That keeps the panel simple, needs no API key, and
means nothing breaks if Google changes the rules.

Two things still come for free, without any key:

**Thumbnails.** `https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg` is a plain URL
pattern, so the preview image appears on its own once the video id is known.
`maxresdefault.jpg` is sharper but is missing on some older uploads;
`hqdefault.jpg` always exists, so prefer it.

**The video id.** Store the id, never the full URL - YouTube URLs come in
several shapes (`watch?v=`, `youtu.be/`, `/live/`, `/shorts/`, plus tracking
parameters). Parse the id out on save and keep only that. It also makes the
embed and thumbnail URLs trivial to build.

**Drop view counts.** They were in the earlier draft because the API could
supply them. Typed by hand they are wrong the day after they are entered, so
the video cards should not show them at all. The placeholder line for views on
the home page and the video page needs removing.

If this ever becomes tedious, the Data API can fill in title, date, duration
and view count from the link alone, or sync the whole channel so new uploads
appear on their own. One free key, 1 quota unit per video against a daily
10,000. Not needed now, just noting it so the option is not rediscovered from
scratch.

## How the public pages get the content

Two options, to decide when building:

1. **Rendered live by PHP.** `/novosti/` becomes `index.php` and reads the
   database on each request. Simplest, but that page stops being static.
2. **Panel triggers a rebuild.** Saving a notice writes the file into `src/`
   and runs the build. Keeps the whole public site static and fast, more moving
   parts to get right.

Option 1 for news and videos only, with everything else staying static, is
probably the right trade. Worth a decision before writing code.

## Rough order of work

1. Get the database credentials from the host
2. `config.php` + `db.php` + `schema.sql`
3. Login, sessions, CSRF, rate limiting
4. Role checks as a single guard used by every admin page
5. News CRUD
6. Video CRUD: paste the link, type the title and date, thumbnail derived
7. Library inventory: books, loans, availability
8. User management for superadmin
9. Wire the public news and video pages to the data
