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



def edit_note(request, id):
    note = get_object_or_404(Note, id=id)

    if request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()
        return redirect('notes_list')

    return render(request, 'core/edit_note.html', {'note': note})




def delete_note(request, id):
    note = get_object_or_404(Note, id=id)
    note.delete()
    return redirect('notes_list')