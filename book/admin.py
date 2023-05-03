from django.contrib import admin
from .models import Bookinfo, Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']

admin.site.register(Bookinfo)
admin.site.register(Book)