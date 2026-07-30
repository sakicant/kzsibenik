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

## Blocker before any of it can be built

It needs **PHP and a MySQL database**. The Vercel preview is static, so the
panel cannot exist there at all - it only works once the site sits on the FTP
host. Before starting:

- [ ] Confirm the FTP host gives us MySQL (or MariaDB) and which PHP version
- [ ] Get the database name, user and password

Without a database the alternative is writing to JSON files on disk. That works
on shared hosting and skips the DB entirely, but it makes concurrent edits and
per-user accounts clumsier. MySQL is the better shape if it is available.

## Open question

The brief lists a **library-only** role, but also says the library stays
static. Those pull against each other. Either the library gets managed through
the panel after all (books table, copies held, copies free, who borrowed what),
or that role is not needed yet. Worth settling before building the roles table.

## Roles

| Role | Can do |
|---|---|
| `superadmin` | Everything, including creating and disabling other accounts |
| `news` | Add, edit and unpublish news notices |
| `video` | Add, edit and remove YouTube videos |
| `library` | See the open question above |

Permissions are checked on every request on the server, not just hidden in the
menu. A `news` user who types the video URL directly gets refused.

## Data

**users** - id, name, email, password_hash, role, active, created_at,
last_login_at

**news** - id, slug, lang, title, body, excerpt, image, tag, published_at,
status (draft/published), author_id, created_at, updated_at

**videos** - id, youtube_id, title, description, published_at, sort_order,
status, author_id

News is bilingual, so either one row per language linked by a shared key, or
HR and EN columns on one row. One row per language matches how `src/pages`
already works.

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

1. Settle the database question and the library role
2. `config.php` + `db.php` + `schema.sql`
3. Login, sessions, CSRF, rate limiting
4. Role checks as a single guard used by every admin page
5. News CRUD
6. Video CRUD
7. User management for superadmin
8. Wire the public news and video pages to the data
