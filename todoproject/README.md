# 📝 Fullstack To-Do List Web Application (Django + HTML, CSS, JS)

A simple **fullstack To-Do List application** built with **Django (backend)** and **HTML, CSS, JavaScript (frontend)**.  


## 🎯 Project Overview

### Core Features
- User Authentication (Sign up, Login, Logout)
- Dashboard for logged-in users
- CRUD Operations on tasks:
  - Add new tasks
  - Edit tasks
  - Mark as completed/uncompleted
  - Delete tasks
- Tasks are stored in the database and tied to the logged-in user
- Responsive UI with clean minimal design
- Flash messages for success/error
- Navigation bar with “Home” & “My Tasks”

### Tech Stack
- **Backend**: Django (Python, Django ORM)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Database**: SQLite (default, for simplicity)

---

## 📦 Setup
```bash
git clone https://github.com/pinchase/todo.git
cd todo
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
