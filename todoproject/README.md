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

## 🔗 URLs
- App: http://127.0.0.1:8000/
