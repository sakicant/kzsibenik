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
- [ ] A YouTube Data API key, so pasting a video link fills in the title, date,
      duration and view count on its own. Free, see the section below.

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
thumbnail_url, view_count, views_checked_at, sort_order, status, author_id

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

## Paste a link, let YouTube fill in the rest

Yes, this works. Paste the URL in the panel, and the title, publish date,
duration, thumbnail and view count come back on their own.

Two ways to fetch, and the difference matters:

| | oEmbed | Data API v3 |
|---|---|---|
| Key needed | no | yes, free |
| Title | yes | yes |
| Thumbnail | yes | yes, several sizes |
| Publish date | **no** | yes |
| View count | **no** | yes |
| Duration | **no** | yes |

oEmbed (`youtube.com/oembed?url=...&format=json`) is the zero-setup option but
gives only the title and thumbnail. Since the design calls for date and view
count, it has to be the **Data API**.

One call per video covers everything:

```
GET https://www.googleapis.com/youtube/v3/videos
    ?part=snippet,statistics,contentDetails&id=VIDEO_ID&key=API_KEY
```

That costs 1 unit against a 10,000 unit daily quota, so it is effectively free
at this scale.

**Fetch on save, not on page load.** When a video is added, call the API once
and write the result into the row. A page that called YouTube on every visit
would be slow, would break whenever YouTube was unreachable, and would burn
quota on every crawler hit.

**View counts are the exception** - they change constantly, so a number stored
once goes stale. Either refresh them on a daily cron across all videos (one
call handles 50 ids at a time, so the whole channel costs 1 unit), or leave
view counts off the page entirely. Worth deciding whether they are wanted at
all; a low count on an old sermon is not necessarily a good look.

**The key must stay server-side.** In `config.php`, which is gitignored, and
never in JavaScript, where anyone could read and use it. Lock the key to the
YouTube Data API and to the server IP in the Google Cloud console.

Getting the key: Google Cloud console, create a project, enable "YouTube Data
API v3", create an API key. Free, no billing card.

**Worth considering:** the same API can list the whole channel's uploads
(`playlistItems.list` on the uploads playlist). "Add a video" could become
"sync the channel", where new uploads appear on their own and the panel is only
used to hide ones that should not show. Fewer steps for whoever maintains it.

Store the video id, never the full URL - YouTube URLs come in several shapes
(`watch?v=`, `youtu.be/`, `/live/`, `/shorts/`, with extra query parameters).
Parse the id out on save and keep that.

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
6. Video CRUD, with the YouTube fetch on save and a daily view-count refresh
7. Library inventory: books, loans, availability
8. User management for superadmin
9. Wire the public news and video pages to the data
