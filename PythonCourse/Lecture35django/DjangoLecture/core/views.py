from django.shortcuts import render

# Create your views here.

from .models import Notes


def notes_list(request):
    notes = Notes.objects.order_by("-created_at")
    return render(request, "core/notes_list.html", {"notes": notes})
