
# 🟦 **Django Lecture 02 — CRUD (Create, Read, Update, Delete)**

**Project:** Notes App
**App:** `core`
**Goal:**
✔ Add — Create Note
✔ Read — List Notes
✔ Update — Edit Note
✔ Delete — Remove Note
✔ Styling included
✔ Full code for all files

---

# ✅ **1. Model (Already Created in Lecture 01)**

We have:

```python
# core/models.py
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

---

# ✅ **2. Create Note (Add New Note)**

## **URL**

```python
# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('add/', views.add_note, name='add_note'),
    path('edit/<int:id>/', views.edit_note, name='edit_note'),
    path('delete/<int:id>/', views.delete_note, name='delete_note'),
]
```

---

## **View**

```python
# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note

def notes_list(request):
    notes = Note.objects.all().order_by('-id')
    return render(request, 'core/notes_list.html', {'notes': notes})

def add_note(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content)
        return redirect('notes_list')
    return render(request, 'core/add_note.html')
```

---

## **Template: Add Note**

`core/templates/core/add_note.html`

```html
{% load static %}
<!doctype html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'core/styles.css' %}">
    <title>Add Note</title>
</head>
<body>

<div class="container">
    <h1 class="heading">Add New Note</h1>

    <form method="POST" class="form-box">
        {% csrf_token %}

        <input type="text" name="title" placeholder="Enter Title" required>
        <textarea name="content" placeholder="Write content..." required></textarea>

        <button type="submit" class="btn">Save Note</button>
    </form>

    <a class="back" href="{% url 'notes_list' %}">← Back to Notes</a>
</div>

</body>
</html>
```

---

# ✅ **3. Read Notes (Already Done)**

But now with **Edit/Delete buttons**:

### `notes_list.html`

```html
{% load static %}
<!doctype html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'core/styles.css' %}">
    <title>Notes</title>
</head>
<body>
<div class="container">

    <h1 class="heading">All Notes</h1>

    <a href="{% url 'add_note' %}" class="btn add-btn">+ Add New Note</a>

    <ul class="note-list">
    {% for note in notes %}
        <li class="note-item">
            <h2>{{ note.title }}</h2>
            <p>{{ note.content }}</p>
            <span class="date">{{ note.created_at }}</span>

            <div class="actions">
                <a href="{% url 'edit_note' note.id %}" class="edit">Edit</a>
                <a href="{% url 'delete_note' note.id %}" class="delete">Delete</a>
            </div>
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

# ✅ **4. Update Note (Edit)**

## **View**

```python
def edit_note(request, id):
    note = get_object_or_404(Note, id=id)

    if request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()
        return redirect('notes_list')

    return render(request, 'core/edit_note.html', {'note': note})
```

---

## **Template**

```html
{% load static %}
<!doctype html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'core/styles.css' %}">
    <title>Edit</title>
</head>
<body>

<div class="container">
    <h1 class="heading">Edit Note</h1>

    <form method="POST" class="form-box">
        {% csrf_token %}

        <input type="text" name="title" value="{{ note.title }}" required>
        <textarea name="content" required>{{ note.content }}</textarea>

        <button type="submit" class="btn">Update</button>
    </form>

    <a class="back" href="{% url 'notes_list' %}">← Back</a>
</div>

</body>
</html>
```

---

# ✅ **5. Delete Note**

```python
def delete_note(request, id):
    note = get_object_or_404(Note, id=id)
    note.delete()
    return redirect('notes_list')
```

---

# 🎨 **6. Update CSS (Add Form + Buttons Styling)**

`core/static/core/styles.css`

Add this at the bottom:

```css
.form-box {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

input, textarea {
    width: 100%;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #bbb;
    font-size: 16px;
}

textarea {
    min-height: 120px;
}

.btn {
    background: #1A73E8;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: 0.2s;
}

.btn:hover {
    background: #1558b0;
}

.add-btn {
    display: inline-block;
    margin-bottom: 20px;
}

.actions a {
    margin-right: 10px;
}

.edit {
    color: #1A73E8;
}

.delete {
    color: #E63946;
}

.back {
    display: block;
    margin-top: 20px;
    color: #333;
}
```

---

# 🎉 **CRUD Lecture Completed**

In this lecture, we created:

✔ Add Note
✔ List Notes
✔ Edit Note
✔ Delete Note
✔ Clean UI with CSS
✔ Fully functional Django app
