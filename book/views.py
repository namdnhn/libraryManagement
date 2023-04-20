from django.shortcuts import render
from django.http import HttpResponse
from .models import Bookinfo

# Create your views here.
def bookpage(request, id):
    book = Bookinfo.objects.get(id=id)
    return render(request, 'bookshowing.html', {'book': book})

def book_list(request):
    books = Bookinfo.objects.all()

    return render(request, 'booklist.html', {
        'books': books
    })