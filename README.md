# SIYAQ — Bilingual Django Blogging Platform

> **SIYAQ (سِياق)** is a robust, production-grade bilingual Django blogging platform developed as part of university assignment **LAB-ORM-1**. It demonstrates comprehensive mastery of core Django concepts, including the Model-View-Template (MVT) architecture, Django ORM, form validation, localization (Arabic/English), persistent cookies, theme switching (Dark/Light mode), and database migrations.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Project Directory Structure](#project-directory-structure)
5. [Installation & Setup](#installation--setup)
6. [Database & Migrations](#database--migrations)
7. [Running the Application](#running-the-application)
8. [Database Model & ORM](#database-model--orm)
9. [Course Concepts Compliance Matrix](#course-concepts-compliance-matrix)
10. [Localization & RTL Support](#localization--rtl-support)
11. [Theme Preferences (Cookies)](#theme-preferences-cookies)
12. [Strict Form Validation](#strict-form-validation)
13. [Django Admin Integration](#django-admin-integration)
14. [Automated Testing](#automated-testing)
15. [Contact & Support](#contact--support)

---

## 1. Project Overview

SIYAQ provides a clean editorial environment for publishing, browsing, searching, and managing articles in both Arabic and English. Built on Django 6.1 and SQLite, the platform adheres strictly to modern web development standards and university curriculum requirements, balancing editorial elegance with rigorous backend validation and secure state management.

---

## 2. Features

- **Dynamic Article Publishing:** Public form allowing creators to publish new articles instantly with strict validation.
- **Publisher Metadata:** Captures and displays publisher names supporting Arabic and English characters.
- **Homepage Feed:** Displays published posts ordered newest-first by default.
- **Article Details:** Dedicated URL route (`/post/<int:post_id>/`) for viewing individual articles with 404 error handling.
- **Search & Sorting:** Real-time query parameter filtering (`?search=...`) and sorting (`?sort=latest` / `?sort=oldest`).
- **Bilingual Interface:** Full Arabic (RTL) and English (LTR) localization with seamless switching.
- **Theme Switcher:** Persistent Light and Dark mode toggling backed by secure cookies.
- **Django Admin:** Comprehensive administrative dashboard for managing posts and translations.

---

## 3. Technologies Used

- **Python 3.14**
- **Django 6.1.3** (Web Framework)
- **SQLite** (Relational Database via Django ORM)
- **HTML5 & CSS3** (Responsive Layouts & Custom Variables)
- **JavaScript** (Interactive UI enhancements)

---

## 4. Project Directory Structure

```text
LAB-ORM-1/
├── blog/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_post_publisher_name.py
│   │   └── 0003_posttranslation.py
│   ├── static/blog/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/
│   ├── templates/blog/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── add_post.html
│   │   └── post_detail.html
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── validators.py
│   └── views.py
├── blogger_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── locale/
│   ├── ar/LC_MESSAGES/django.po
│   └── en/LC_MESSAGES/django.po
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## 5. Installation & Setup

1. **Clone or Open Repository:**
   Navigate to the project root directory.

2. **Create and Activate Virtual Environment (Windows PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies:**
   ```powershell
   python -m pip install -r requirements.txt
   ```

---

## 6. Database & Migrations

Verify migration status and apply database schema:

```powershell
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
python manage.py migrate
```

To inspect specific migration SQL:
```powershell
python manage.py sqlmigrate blog 0001
```

---

## 7. Running the Application

Start the development server:

```powershell
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/` (automatically redirects to `/home/`).

### Primary Public Routes:
- `/` — Root redirect to homepage
- `/home/` — Article feed with search & sorting
- `/about/` — About SIYAQ editorial overview
- `/add/` — Public article submission form
- `/post/<int:post_id>/` — Individual article view
- `/admin/` — Django Administration panel

---

## 8. Database Model & ORM

### Core `Post` Model (`blog/models.py`)
```python
class Post(models.Model):
    publisher_name = models.CharField(max_length=150, blank=True, default="")
    title = models.CharField(max_length=2048)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
```

### Django ORM Usage Examples
- **Retrieving Published Posts:**
  ```python
  posts = Post.objects.filter(is_published=True).order_by('-published_at')
  ```
- **Searching Articles:**
  ```python
  posts = Post.objects.filter(
      Q(title__icontains=query) | Q(content__icontains=query)
  )
  ```
- **Creating a Record:**
  ```python
  Post.objects.create(publisher_name="أحمد", title="عنوان", content="محتوى...")
  ```

---

## 9. Course Concepts Compliance Matrix

| Studied Topic | Implementation File | Verification Result |
|---|---|---|
| Apps & Views | `blog/views.py` | PASS |
| Templates | `blog/templates/blog/*.html` | PASS |
| Static Files | `blog/static/blog/` | PASS |
| MVT Architecture | `blog/models.py`, `views.py`, `templates/` | PASS |
| URL Mapping | `blogger_project/urls.py`, `blog/urls.py` | PASS |
| URL Resolving | `{% url %}`, `reverse()` | PASS |
| Template Inheritance | `blog/templates/blog/base.html` | PASS |
| Cookies | `blog/views.py` (Theme & Lang) | PASS |
| Path Parameters | `blog/urls.py` (`<int:post_id>`) | PASS |
| Query Parameters | `blog/views.py` (`request.GET`) | PASS |
| Django ORM | `blog/models.py`, `views.py` | PASS |
| Migrations | `blog/migrations/` | PASS |

---

## 10. Localization

SIYAQ supports Arabic (`ar`) and English (`en`) through Django's `LocaleMiddleware` and translation files (`.po`). Language preferences persist via `django_language` cookies and automatically adapt layout directions (RTL for Arabic, LTR for English).

---

## 11. Theme Preferences (Cookies)

Theme toggling between Light and Dark mode is managed via cookies (`theme=light` or `theme=dark`) set in `blog/views.py` and read via `blog/context_processors.py`. Preferences persist across navigation, page refreshes, and language switches.

---

## 12. Strict Form Validation

Validation rules (`blog/validators.py`) ensure data integrity:
- **Publisher Name:** Required, 2–150 characters, alphabetic letters supported (Arabic/English), strictly rejects numbers-only or symbols-only input.
- **Article Title:** Required, 5–2048 characters, rejects numbers-only or symbols-only input.
- **Article Content:** Required, minimum 30 non-whitespace characters, rejects numbers-only or symbols-only input.

---

## 13. Django Admin Integration

Manage platform data securely via Django Admin:
```powershell
python manage.py createsuperuser
```
Access at `http://127.0.0.1:8000/admin/`.

---

## 14. Automated Testing

Execute the test suite and system checks:
```powershell
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```
*Result:* 17 unit and integration tests passing successfully (100% pass rate).

---

## 15. Contact & Support

- **Developer / Maintainer Discord:** [Click Here](https://discord.com/users/686267127807606819)
- **Assignment:** LAB-ORM-1 | SIYAQ (سِياق)
