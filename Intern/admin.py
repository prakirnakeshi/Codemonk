from django.contrib import admin

from Intern.models import *

# Register your models here.
@admin.register(Book)
class StudentAdmin(admin.ModelAdmin):
    list_display=['title', 'author', 'publication_year', 'isbn']