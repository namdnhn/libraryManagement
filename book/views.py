from datetime import datetime
from django.shortcuts import render
from .models import Bookinfo
from django.db.models import Q


# Create your views here.
def bookpage(request, id):
    book = Bookinfo.objects.get(id=id)
    expiredAccount = False
    if not request.user.user.expired_date or request.user.user.expired_date < datetime.now().date():
        expiredAccount = True
    return render(request, 'bookshowing.html', {'book': book, 'expiredAccount': expiredAccount})


def book_list(request):
    books = Bookinfo.objects.all()

    return render(request, 'booklist.html', {
        'books': books
    })


def search(request):
    if 'q' in request.GET:
        q = request.GET.get('q')
        books = Bookinfo.objects.order_by('-title').filter(Q(title__icontains=q) | Q(description__icontains=q))
        book_count = books.count()
    return render(request, 'booksearch.html', {
        'books': books,
        'q': q,
        'book_count': book_count
    })
