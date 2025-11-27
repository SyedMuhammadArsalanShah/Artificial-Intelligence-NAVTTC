
# 📘 Django First Lecture — Complete Step-by-Step Project

This project is the final output of **Django Lecture 01**, where you learn how to set up Django from zero and build a complete working mini-application with:

✔ Virtual environment
✔ Django installation
✔ Project + App creation
✔ Database migrations
✔ Admin panel setup
✔ Model
✔ View
✔ Template
✔ Static CSS styling
✔ URL routing

---

## 🚀 Learning Objectives

By the end of this lecture, you will be able to:

* Understand Django’s **MTV architecture**
* Create a project & app
* Create and manage models
* Use Django’s built-in admin panel
* Build templates and views
* Add and load static CSS files
* Run the Django development server

---

# 🛠 1. Setup & Installation

### Create project folder

```bash
mkdir django-first-lecture
cd django-first-lecture
```

### Create & activate virtual environment

**Windows (PowerShell):**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### Install Django

```bash
pip install django
python -m django --version
```

---

# 📂 2. Create Django Project

```bash
django-admin startproject mysite .
```

This creates:

```
manage.py
mysite/
    settings.py
    urls.py
    asgi.py
    wsgi.py
```

Run development server:

```bash
python manage.py runserver
```

Visit:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

# 📂 3. Create App

```bash
python manage.py startapp core
```

Add to **mysite/settings.py**:

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'core',
]
```

---

# 🧱 4. Create Model

Edit `core/models.py`:

```py
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 🔐 5. Django Admin Setup

Create superuser:

```bash
python manage.py createsuperuser
```

Register model — `core/admin.py`:

```py
from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
```

Admin panel:

👉 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

# 🌐 6. Views & Templates

### View (core/views.py)

```py
from django.shortcuts import render
from .models import Note

def notes_list(request):
    notes = Note.objects.order_by('-created_at')
    return render(request, 'core/notes_list.html', {'notes': notes})
```

---

### Template Structure

Create folder:

```
core/
└── templates/
    └── core/
        └── notes_list.html
```

HTML template (`notes_list.html`):

```html
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Notes</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'core/styles.css' %}">
</head>
<body>
    <div class="container">
        <h1 class="heading">Notes</h1>

        <ul class="note-list">
            {% for note in notes %}
                <li class="note-item">
                    <h2>{{ note.title }}</h2>
                    <p>{{ note.content }}</p>
                    <span class="date">{{ note.created_at }}</span>
                </li>
            {% empty %}
                <li class="empty">No notes available.</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
```

---

# 🎨 7. Static CSS Styling

Create folder:

```
core/
└── static/
    └── core/
        └── styles.css
```

**styles.css**

```
body {
    margin: 0;
    padding: 0;
    background: #f7f9fc;
    color: #333;
    font-family: Arial, sans-serif;
}

.container {
    width: 80%;
    max-width: 900px;
    margin: 40px auto;
}

.heading {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 30px;
}

.note-list {
    list-style: none;
    padding: 0;
}

.note-item {
    background: #fff;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
}

.note-item h2 {
    margin: 0 0 10px;
    font-size: 22px;
}

.note-item p {
    margin: 0 0 15px;
}

.date {
    font-size: 12px;
    color: #777;
}

.empty {
    text-align: center;
    color: #777;
    font-style: italic;
}
```

---

# 🔗 8. URL Routing

Create `core/urls.py`:

```py
from django.urls import path
from .views import notes_list

urlpatterns = [
    path('', notes_list, name='notes_list'),
]
```

Include in **mysite/urls.py**:

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
```

---

# 🧪 9. Run the Project

```bash
python manage.py runserver
```

Visit:

👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)
👉 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

# 📌 10. Commands Summary

| Purpose           | Command                                                        |
| ----------------- | -------------------------------------------------------------- |
| Create venv       | `python -m venv venv`                                          |
| Activate venv     | `source venv/bin/activate` or `.\\venv\\Scripts\\Activate.ps1` |
| Install Django    | `pip install django`                                           |
| Create project    | `django-admin startproject mysite .`                           |
| Create app        | `python manage.py startapp core`                               |
| Make migrations   | `python manage.py makemigrations`                              |
| Apply migrations  | `python manage.py migrate`                                     |
| Create admin user | `python manage.py createsuperuser`                             |
| Run server        | `python manage.py runserver`                                   |

---

# 🎯 Homework (For Students)

✔ Create a new page: `/note/<id>/` (detail page)
✔ Add a form to create notes
✔ Add edit/delete functionality (CRUD)
✔ Add Bootstrap or Tailwind styling


