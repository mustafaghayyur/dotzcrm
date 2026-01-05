# GitHub Copilot / AI Agent Instructions for Dotz CRM + PM Software 🔧

## Purpose
Concise, actionable guidance to get an AI coding agent productive in this repository quickly. Focus on the architecture, developer workflows, and project-specific conventions (not general best practices).

## Big picture (what to know first) ✅
- Monolithic Django app (Django 5.2.7), with modular apps: `core`, `tasks`, `tickets`, `documents`, `customers`, `restapi`. See `project/settings.py` for installed apps.
- All Create/Update/Delete operations must go through the REST API single-entry point (`restapi/`). See `restapi/README.md`. Other views are read-only.
- The project uses a Data Relationship Manager (DRM) layer for CRUD: `core/DRMcore/README.md`. DRMs wrap raw SQL querysets — **ALL** CRUD should be implemented/modified in DRM + DRM.querysets, not ad-hoc in models/views.

## Project-specific rules & examples ⚠️
- LAWS OF CRUD: Only DRM files (and their `querysets`) should perform DB CUD operations. If a CRUD operation is missing, add it to the DRM and the related `DRM.querysets` raw SQL files. (See `core/DRMcore/README.md`.)
- Do not change Django model classes except when changing DB schema (and then create a migration). Models represent the canonical DB structure.
- REST API rule: CUD through `restapi` app; views outside `restapi` should only read data and return results via `context.results` where applicable. (See `restapi/README.md`.)

## Developer workflows (commands & examples) 🔧
- Python/Django dev:
  - Run server or management commands via `manage.py` (standard Django commands). Example: `python manage.py runserver` or `python manage.py migrate`.
  - DB: MySQL (see `project/settings.py` DATABASES). See `CRM-DOCUMENTATION/7.MySQL-Server-Settings.md` for recommended server options.
  - Settings: `DEBUG` is `True` in `project/settings.py` by default for local dev — **do not** leave `DEBUG=True` in production.
- Frontend build (in `static/`):
  - Install deps: `cd static && npm install`.
  - Build bundles: `npm run build`, `npm run build:core`, `npm run build:tasks` (see `static/package.json` and `static/README.md`).
  - Sass: `sass ./scss/dotzstrap.scss:./css/dotzstrap.css` (or `sass --watch` in development).
  - Webpack entries: `core` and `tasks` (see `static/README.md` examples and `webpack.config.js` if present).

## Logs & debugging 💡
- CRUD logging: `core/settings.py` documents `tasks['crud_logger_file']` — check the file path (defaults to `/Users/mustafa/Sites/python/server1/CRUD.log`). CRUD operations are logged when Django `DEBUG` is enabled.
- HTTP & server logs are under `logs/httpd/` and MySQL logs under `logs/mysqld/`.

## Integration points & dependencies 🔗
- MySQL (Connector/Python present in env); Django uses `django.db.backends.mysql` in `project/settings.py`.
- mod_wsgi is the expected production deployment model (see top-level README).
- REST Framework (`rest_framework`) used by `restapi` app.

## Conventions for AI code edits ✍️
- If changing DB behavior, always update both:
  1. The DRM operation (e.g., `core/DRMcore/tasks.py` or app-specific DRM modules)
  2. The matching `DRM.querysets` raw SQL (where applicable)
- If adding APIs: add endpoints inside `restapi/` and ensure CUD operations call DRM methods rather than modifying models directly.
- Use explicit file references in suggestions (e.g., “modify `core/DRMcore/querysets/tasks/*.sql` to include ...”).

## Where to look first (quick file pointers) 📎
- Architecture & rules: `core/DRMcore/README.md`, `restapi/README.md`, `CRM-DOCUMENTATION/` (esp. `APPENDIX-OF-TERMS.md` and MySQL settings)
- Settings & DB: `project/settings.py`, `core/settings.py`
- Frontend build: `static/README.md`, `static/package.json`
- Entry points: `manage.py`, `project/urls.py`, top-level `README.md`

## When in doubt
- Prefer adding/altering DRM + querysets over editing models or direct DB access.
- If a REST API endpoint is required for CUD, add it to `restapi/` and make it call DRM methods.

---
If you'd like, I can open a PR creating this file and include a short changelog entry; otherwise tell me any missing/incorrect bits and I'll revise the instructions. ✅
