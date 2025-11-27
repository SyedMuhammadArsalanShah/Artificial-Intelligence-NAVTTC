from django.contrib import admin

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display=('title','created_at')
    search_fields=('title','contents')