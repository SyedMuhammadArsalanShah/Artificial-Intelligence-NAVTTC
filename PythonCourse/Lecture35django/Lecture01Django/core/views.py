

# Create your views here.
from django.shortcuts import render
from .models import Note

def notes_list(request):
    notes = Note.objects.order_by('-created_at')
    return render(request, 'core/notes_list.html', {'notes': notes})