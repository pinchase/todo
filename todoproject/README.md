# 📝 Fullstack To‑Do List Web App (Django + HTML/CSS/JS)

Lightweight to‑do app with Django backend and a minimal HTML/CSS/JS frontend. Authenticated users can manage their own tasks.

## 🎯 Features
- Sign up, login, logout
- Dashboard for logged‑in users
- Tasks: add, edit, mark complete/incomplete, delete
- Flash messages and responsive UI

## 🧰 Tech Stack
- Backend: Django (Python, Django ORM)
- Frontend: HTML, CSS, Vanilla JS
- Database: MySQL (local via .env) or any DB via DATABASE_URL

## 🚀 Setup
From the repository root:

```bash
# 1) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2) Install dependencies
cd todoproject
pip install -r requirements.txt


# 3) Apply migrations and run
python manage.py migrate
python manage.py runserver
```

Optional:
- Create admin user: `python manage.py createsuperuser`

🔗 URLs

Local App: http://127.0.0.1:8000/

Admin Panel: http://127.0.0.1:8000/admin/

📩 Email Verification (how it works)

On sign-up, the app sends a verification email with a time-limited link.

Accounts remain inactive until verified.

Users can request the verification email to be resent.

🔮 Future (planned / fictional) features

These are ideas for later — mostly fictional and aspirational.

Real-time collaborative lists (WebSocket-driven live edits)

Native mobile apps (iOS & Android) with background sync

Push notifications & scheduled reminders

Smart AI task suggestions and automatic scheduling

Google / Outlook calendar sync

Team workspaces with roles & granular permissions

Offline-first PWA with background sync & conflict resolution

Attachments with OCR (convert photos to tasks)

CSV import/export, backup & restore

Integrations: Slack, Notion, Trello

OAuth / SSO (Google, GitHub, SAML for enterprise)

Multi-language localization & region settings

Analytics & productivity dashboard (time-spent, completion rates)

Dark mode and customizable themes

🧾 Notes

superuser.json (fixture) should not be auto-loaded on every deploy; treat fixtures as one-time seeds or use a safe seeding strategy.

Keep secrets (EMAIL_HOST_PASSWORD, DATABASE credentials) out of the repo; use Render/Env vars for production.
