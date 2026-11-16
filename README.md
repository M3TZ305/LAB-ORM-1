# SIYAQ | سِياق

A lightweight Arabic-only Django university blog. The public interface always uses Arabic and RTL, regardless of browser language or old language cookies. User-authored articles, including English text, are preserved.

## Install and run

Use the single project folder `labs/LAB-ORM-1`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Visit `/home/`. Root `/` redirects there. Other public routes are `/about/`, `/add/`, `/post/<id>/`, `/post/<id>/edit/`, `/post/<id>/delete/`. Theme changes use CSRF-protected POST. Old `/ar/` and `/en/` article routes redirect to canonical routes and preserve query parameters; unknown legacy paths return 404. There is no language switching endpoint.

## Public article management

Public login, logout and signup have been removed. All visitors may create, edit and delete published articles, as explicitly requested for this shared university project. This deliberately means visitors can change or permanently delete each other's content. CSRF protection, field/upload validation and a separate POST-only delete confirmation remain in place. Unpublished articles remain unavailable through public article routes. Django Admin authentication and existing account/owner metadata are retained to preserve records, but ownership no longer restricts published article management.

Edit/delete controls appear inside article details. Original article IDs and publishing timestamps are preserved. Dates display date and time explicitly in Asia/Riyadh. The About page describes the educational project and its actual public workflow.

## Models and migrations

`blog.Post` retains `title(max_length=2048)`, `content`, `is_published(default=True)`, `published_at(auto_now_add=True)` and publisher name. It adds a nullable User foreign key with SET_NULL.

Migration `blog.0004` preserves original posts and independently copies any distinct Arabic translation into an additional Post with its original publisher and timestamp before removing the obsolete translation table. Original titles/content are never overwritten. Translation removal is irreversible as a data operation: restore the SQLite backup if you need the original translation records. Migration history is retained. The installed database originally had no translation records.

`media_library.PostAttachment` belongs to Post with CASCADE. Fields: file, safe display filename, validated MIME type, upload timestamp and featured flag. A conditional unique constraint allows at most one featured attachment per post. `media_library.0001` creates this model.

Always back up SQLite before applying schema changes. Do not reset the database or fake migration status.

## Attachments

Supported formats: JPG/JPEG, PNG, WEBP, GIF, PDF, UTF-8 TXT, DOCX, XLSX and PPTX. Defaults: 10 MiB per file and five total attachments per article, configurable as `MAX_ATTACHMENT_SIZE` and `MAX_POST_ATTACHMENTS`. Pillow verifies image formats/dimensions. PDF headers/end markers, UTF-8 text and Office archive structure are checked; Office archives have entry, expansion and compression-ratio limits. Executables, HTML, SVG, scripts, macro-enabled formats and extension/content mismatches are rejected. These checks are not an antivirus or a document sanitizer: deployments needing malware scanning must add it.

Uploads use Django storage under `MEDIA_ROOT = BASE_DIR / 'media'`, with UUID filenames under `posts/<post_id>/`. User files are ignored by Git. Static fallback article images remain untouched. Forms accept multiple attachments and show selected filenames. Users can select existing files for removal and select a cover or the first newly uploaded image. Invalid forms retain text; browsers require file re-selection.

Article and attachment changes use a transaction. Failed new uploads are removed on rollback; attachment deletions schedule file cleanup only after database commit. Storage cleanup errors are logged and may require manual removal of orphan files. Upload I/O failures return an Arabic form error.

`/media/<attachment_id>/` serves validated files through a permission-aware FileResponse in development and production. Images and PDF support preview; other documents use attachment disposition. Responses include `nosniff` and a sandbox CSP; raw storage paths are never exposed. Do not configure a public catch-all media route or web-server alias that bypasses draft permissions. For large deployments use a private storage service/internal redirect after the same authorization check.

## Design

Full-width header, main background and compact footer; responsive inner container up to 1400px. Two article columns on desktop and one on mobile. Alexandria Bold brand, Cairo headings and IBM Plex Sans Arabic UI/body use Google Fonts with system fallbacks. Light/dark themes persist through a validated cookie. Search and chronological sorting remain GET query parameters.

## Verification

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py showmigrations
```

Tests cover article validators, Arabic routing, CRUD, public edit/delete behavior, CSRF, unpublished records, authentication, search, sort, theme cookies and attachment validation/storage cleanup. Media tests use temporary storage, never the real media directory.

## LAB-ORM-1 coverage

The project retains Django apps/views, MVT, inherited templates, static files, named URL resolution, redirects, path/query parameters, cookies, Django ORM, SQLite, migration history and original article fields. Media and authorization extend this structure without a frontend framework or external authentication package.

Development server and DEBUG are for local use only. Before public deployment configure a secret key, allowed hosts, HTTPS, secure cookies, production WSGI/ASGI service and private media storage. Uploaded documents may contain untrusted content. Contact: https://discord.com/users/686267127807606819

## Single publication timestamp

`published_at` is the only active article date field. It defaults to the current time and can be entered or edited through a required datetime-local field interpreted in Asia/Riyadh. Django stores aware timestamps in UTC and converts to Riyadh for display and input. Migration 0006 removes the redundant date field without changing existing published_at values. Earlier migrations remain as historical records.
