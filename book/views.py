from django.shortcuts import render
from .models import Bookinfo
from django.db.models import Q


# Create your views here.
def bookpage(request, id):
    book = Bookinfo.objects.get(id=id)
    return render(request, 'bookshowing.html', {'book': book})


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
