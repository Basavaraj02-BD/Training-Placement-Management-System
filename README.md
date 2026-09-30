# TrackPoint — Training & Placement Management System

A full-stack Django web app for a training institute to manage students, batches,
attendance, mock tests, mock interviews, projects, and placements from one platform.

## Tech stack

- **Backend:** Python 3 / Django 6 (server-rendered — no separate API layer needed)
- **Database:** SQLite by default (zero setup). Swapping to PostgreSQL/MySQL is a
  one-block change in `config/settings.py` (`DATABASES`) — the ORM code doesn't change.
- **Frontend:** Django templates + Bootstrap 5, custom design system in `static/css/style.css`
- **Auth:** Django's built-in auth with a custom `User` model (`accounts.User`) carrying
  an Admin/Trainer role

## Quick start

```bash
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000/ — the database is already migrated and seeded with demo data.

**Demo logins**
| Role    | Username | Password    |
|---------|----------|-------------|
| Admin   | admin    | Admin@123   |
| Trainer | trainer1 | Trainer@123 |
| Trainer | trainer2 | Trainer@123 |

To start from a clean database instead: delete `db.sqlite3`, then run
`python manage.py migrate` and `python manage.py seed_demo` (or skip seeding and use
`python manage.py createsuperuser`).

## Modules

| Module | What it covers |
|---|---|
| **Students** | Registration, profile, course/batch assignment, contact info, status, per-student history (attendance, tests, interviews, projects, applications) in one detail view |
| **Batches** | Create/manage batches, course + trainer assignment, timing, roster |
| **Attendance** | Daily present/absent marking per batch, history, batch-wise % report, low-attendance list (<75%) |
| **Mock tests** | Schedule by batch/topic/date, bulk mark entry, per-test results, per-student performance history |
| **Mock interviews** | Schedule (Technical/HR), attendance, feedback + score as a separate step |
| **Projects** | Title/team/dates, status tracking, trainer evaluation + score |
| **Placements** | Companies, job postings (role, code, CTC), applications with interview/selection status and offer CTC |
| **Dashboard** | Totals, today's & overall attendance %, upcoming tests/interviews, pending projects, placement pipeline |

## Roles

- **Admin** — full access everywhere, including batches, companies, job postings and
  applications, plus Django admin (`/admin/`) for user management.
- **Trainer** — full CRUD on students, attendance, mock tests, interviews and projects
  (the day-to-day training work); read-only on batches and placements, which stay with
  the placement cell/admin. Enforced server-side in `accounts/mixins.py`, not just hidden
  in the UI.

## Demonstrating the full flow

Log in as `admin` and walk: **Students → add a student** → **Batches → view roster** →
**Attendance → mark today's attendance for a batch** → **Mock tests → schedule one →
record results** → **Mock interviews → schedule → add feedback** → **Projects → evaluate** →
**Placements → Applications → update selection status/offer CTC**. The seed data already
has one of each so you can see real numbers on the dashboard immediately, and the flow
above shows it working live.

## Notes / possible next steps

- Student photos use Django's `ImageField` (Pillow) — none are seeded, so add one via
  Students → Edit to see it in action.
- There's no separate student-facing login/portal (view-only own attendance/results) —
  everything here is the staff/institute side, which is what the brief's modules describe.
  That's a natural v2 addition if self-service is needed.
- `SECRET_KEY` in `config/settings.py` is a dev-only placeholder — replace it before any
  real deployment, along with `DEBUG=False` and a real `ALLOWED_HOSTS`.

## Design refresh (v2)

The UI was upgraded to a dark-mode-first, "advanced modern" look on top of the same
Django views/URLs/forms — nothing in the backend changed.

- **Theme:** dark by default, light/dark toggle in the topbar (persisted in `localStorage`).
  Tokens live in `static/css/style.css` as CSS variables (`:root` = light, `[data-theme="dark"]`
  = dark overrides).
- **Glass surfaces:** cards/tables/forms use `backdrop-filter: blur()` with hairline borders
  instead of flat borders/shadows.
- **Charts:** the dashboard now renders a 14-day attendance trend line and a placement-pipeline
  bar chart with Chart.js (CDN), fed by `dashboard/views.py`.
- **Command palette:** press `Ctrl/Cmd+K` anywhere to jump to any module.
- **Toasts:** Django's messages now render as dismissing toasts instead of static banners.
- **Segmented toggle:** attendance marking uses an animated Present/Absent pill control.
- **Sidebar:** icon + label nav with a collapse button (desktop) and the existing slide-out
  behavior on mobile.

All of this is vanilla JS (`static/js/app.js`) plus Chart.js — no build step, no new Python
dependencies, so `requirements.txt` is unchanged.
